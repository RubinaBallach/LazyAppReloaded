import time
import re
import requests
from bs4 import BeautifulSoup
from openai import OpenAI


class FlatAdImporter:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }

    def retrieve_information(self):
        """switchboard to select the correct method for information retrieval based on the URL"""
        if "immowelt" in self.url:
            return self.get_immowelt_information()
        else:
            raise ValueError(f"Unsupported URL: {self.url}, please enter information manually.")
        
    def soup_decorator(func):
        """
        Decorator to manage a BeautifulSoup object for data scraping.

        Args:
            func: The function to be decorated.

        Returns:
            A wrapper function that handles BeautifulSoup setup and teardown.
        """
        def wrapper(self, *args, **kwargs):
            website = requests.get(self.url, headers=self.headers)
            try:
                self.soup = BeautifulSoup(website.text, "html.parser")
                result = func(self, *args, **kwargs) # call the decorated function
                return result
            except Exception as e:
                print(f"Error during information retrieval: {e}")
        return wrapper

    @soup_decorator
    def get_immowelt_information(self):
        """Retrieve information from an Immowelt listing."""
        data = {}

        #Extracting the title of the flat description
        title_element = self.soup.find("h1", class_="ng-star-inserted")
        data["title"] = title_element.text.strip() if title_element else None

        # Extracting City, Postal Code and District
        address_element = self.soup.find("span", {"data-cy": "address-city"})
        if address_element:
            address_text = address_element.text.strip()
            address_match = re.match(r"(\d{5})\s*([^\(]+)\s*\(([^)]+)\)", address_text)
            if address_match:
                data["postal_code"] = address_match.group(1)
                data["city"] = address_match.group(2).strip()
                data["district"] = address_match.group(3).strip()

        # Extracting the cost without extra costs and heating costs
        kaltmiete_element = self.soup.find("strong", class_="ng-star-inserted")
        data["kaltmiete"] = (kaltmiete_element.text.strip()
                             if kaltmiete_element else "n/a")


        # Extracting the space of the flat
        space_element = self.soup.find("span", class_="has-font-300")  # fläche
        data["apartment_size"] = space_element.text.strip() if space_element else "n/a"

        # Extracting the deposit of the flat
        deposit_element = self.soup.find("p", class_="card-content")
        deposit_value = deposit_element.text.strip() if deposit_element else None
        data["deposit"] = f"{deposit_value} €" if deposit_value else "n/a"

        # Extracting the no of rooms of the flat
        rooms_element = self.soup.find("span", class_="has-font-300")
        for _ in range(7):
            rooms_element = rooms_element.next_element
        data["rooms"] = rooms_element.text.strip() if rooms_element else "n/a"

        # Extracting the extra costs
        extra_costs_element = self.soup.find(
            "sd-cell-col", class_="cell__col is-pulled-right"
        )
        for _ in range(13):
            extra_costs_element = extra_costs_element.next_element
        data["extra_costs"] = extra_costs_element.text.strip() if extra_costs_element else "n/a"

        # Extracting the heating costs
        heating_costs_element = self.soup.find(
            "sd-cell-col", class_="cell__col is-pulled-right"
        )
        for _ in range(18):
            heating_costs_element = heating_costs_element.next_element
        data["heating_costs"] = heating_costs_element.text.strip() if heating_costs_element else "n/a"

        # Extracting the total cost
        total_cost_element = self.soup.find(
            "sd-cell-col", class_="cell__col is-pulled-right")
        for _ in range(35):
            total_cost_element = total_cost_element.next_element
        data["total_cost"] = total_cost_element.text.strip() if total_cost_element else "n/a"

        data["landlord_name"] = self.soup.find('p', class_='offerer').get_text(strip=True)     
        data["landlord_contact"] = self.soup.find('p', class_='is-bold').get_text(strip=True)
        data["landlord_address"] =  self.soup.find('p', {'data-cy': 'offerer-address'}).get_text(strip=True)

        return data


class FlatApplicationLetterGenerator:
    def __init__(self, api_key, flat_application_data, lazy_renter_data, landlord_data):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.flat_app_data = flat_application_data
        self.lazy_renter_data = lazy_renter_data
        self.landlord_data = landlord_data

    def generate_prompt(self):
        prompt = f"""
        Entwerfe ein Anschreiben für eine Wohnungsbewerbung. 
        Die Wohnung hat {self.flat_app_data["rooms"]} Zimmer und eine Wohnfläche von {self.flat_app_data["apartment_size"]}.
        Die Kaltmiete beträgt {self.flat_app_data["kaltmiete"]},die Gesamtmiete von {self.flat_app_data["total_cost"]}.
        Wenn du etwas über den Standort der Wohnung in {self.flat_app_data["district"]},{self.flat_app_data["city"]}, weißt, 
        begründe warum du dort wohnen möchtest.

        **Informationen zu Mietinteressenten:**
        - Vollständiger Name: {self.lazy_renter_data["first_name"]} {self.lazy_renter_data["last_name"]}
        - Geburtsdatum: {self.lazy_renter_data["date_of_birth"]}
        - Aktuelle Adresse: {self.lazy_renter_data["current_address"]}
        - Email: {self.lazy_renter_data["renter_mail"]}
        - Beruf: {self.lazy_renter_data["current_occupation"]}
        - Monatliches Netto-Einkommen: {self.lazy_renter_data["net_income"]} €"""
        if self.lazy_renter_data["stable_income_available"]:
            prompt += "\n- Gesichertes Einkommen verfügbar"
        if self.lazy_renter_data["guarantee_available"]:
            prompt += "\n- Bürgschaft verfügbar"
        if self.lazy_renter_data["clean_schufa_report"]:
            prompt += "\n- Saubere Schufa-Auskunft"
        if self.lazy_renter_data["references_available"]:
            prompt += "\n- Mietschuldenfreiheitsberscheinigung vorhanden"
        if self.lazy_renter_data["long_term_leasing_desire"]:
            prompt += "\n- Wunsch nach einer langfristing Anmietung"
        else:
            prompt += "\n- Wunsch nach einer kurz- bis mittelfrisitigen Anmietung"
        if self.lazy_renter_data["quiet_and_tidy_tenant"]:
            prompt += "\n- Ruhiger und ordentlicher Mieter"
        if self.lazy_renter_data["children"] == True:
            prompt += f"\n- Kinder : {self.lazy_renter_data['no_of_children']}"
        else:
            prompt += "\n- keine Kinder"
        if self.lazy_renter_data["pets"] == True:
            prompt += f"\n- Haustiere: {self.lazy_renter_data['type_of_pets']}"
        else:
            prompt += "\n- keine Haustiere"
        prompt += f"""
                \n- Anzahl der Personen, die einziehen: {self.lazy_renter_data['no_of_people']}"""
        if self.flat_app_data["additional_notes"]:
            prompt +=f"""Berücksichtige folgende Anmerkungen im Anschreiben: {self.flat_app_data["additional_notes"]}."""
        prompt +=f"""    
        Das Anschreiben für die Wohnungsbewerbung soll in deutscher Sprache verfasst werden.
        Hier ist ein Beispiel für das gewünschte Format.
        Berücksichtige die oben genannten Informationen und füge sie an den richtigen Stellen ein:

        [vollständiger Name]
        [Adresse]
        [Telefonnummer]
        [Email]

        Vermieter
        {self.landlord_data['landlord_name']}
        {self.landlord_data['landlord_contact']}
        {self.landlord_data['landlord_address']}


        <Heutiges Datum ergänzen>

        Bewerbung für die {self.flat_app_data["rooms"]} -Zimmer-Wohnung in {self.flat_app_data["city"]} 

        Sehr geehrte Damen und Herren,
        """
        if self.lazy_renter_data['no_of_people'] == 1:
            prompt += f"""
            Ich, {self.lazy_renter_data["first_name"]} {self.lazy_renter_data["last_name"]} möchte mich für die oben genannte Wohnung bewerben und mich kurz vorstellen.
            Ich bin als  {self.lazy_renter_data["current_occupation"]} beschäftigt und verfüge über ein Nettoeinkommen von monatlich {self.lazy_renter_data["net_income"]} €
            Die Gehaltsabrechnungen habe ich beigefügt
                        """
        else:
            prompt += f"""
            Wir, Familie {self.lazy_renter_data["last_name"]} möchten uns für die oben genannte Wohnung bewerben und uns kurz vorstellen.
            Wir sind als {self.lazy_renter_data["current_occupation"]} beschäftigt und verfügen über ein gemeinsames Nettoeinkommen von monatlich {self.lazy_renter_data["net_income"]} €
            Die Gehaltsabrechnungen haben wir beigefügt
            """
            if self.lazy_renter_data['no_of_children']>0:
                prompt+=f"""
                Wir haben {self.lazy_renter_data['no_of_children']} Kinder. {{...expandiere hier...}} 
                Jetzt, da das/die Kind(er) größer sind und ein eigenes Zimmer bekommen sollen, 
                reicht der Platz in unserer derzeitigen Wohnung nicht mehr aus.
                """
        
        prompt +=f"""
            Die angebotene {self.flat_app_data["rooms"]}-Zimmer-Wohnung entspricht in Größe, Schnitt und Lage genau meinen/unseren Vorstellungen. 
            {self.flat_app_data["additional_notes"] if self.flat_app_data["additional_notes"] else ""}
            Ich/Wir freuen uns auf die Möglichkeit, die Wohnungzu besichtigen und ein persönliches Gespräch.

            Mit freundlichen Grüßen,
            {self.lazy_renter_data["first_name"]} {self.lazy_renter_data["last_name"]}

            Anlagen:
            - Gehaltsabrechnungen
            {'- SCHUFA-Auskunft' if self.lazy_renter_data["clean_schufa_report"] == True else ''}
            {'- Mietschuldenfreiheitsbescheinigung' if self.lazy_renter_data["references_available"] else ''}
            {'- Nachweis über Bürgschaft' if self.lazy_renter_data["guarantee_available"] else ''}
            """

        return prompt
    
    def generate_flat_application_letter(self):
        start_time = time.time()
    
        prompt = self.generate_prompt()
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Du bist ein hilfreicher KI Assistent, der eine Bewerbung für eine Wohnung schreibt.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"\nTime Consumed: {elapsed_time:.2f} seconds")
        flat__application_letter = response.choices[0].message.content.strip()
        
        return flat__application_letter

# if __name__ == "__main__":
#     # Replace "YOUR_API_KEY" with your actual OpenAI API key
#     openai.api_key = ""

#     """# Example usage
#     user_criteria = {
#         "full_name": "Max Mustermann",
#         "date_of_birth": "1990-01-01",
#         "current_address": "Musterstraße 1",
#         "marital_status": "Single",
#         "current_occupation": "Software Developer",
#         "monthly_income": 3000,
#         "stable_income_available": True,
#         "guarantee_available": False,
#         "clean_schufa_report": True,
#         "references_available": True,
#         "long_term_leasing_desire": True,
#         "quiet_and_tidy_tenant": True,
#         "pets": False,
#         "phone_number": "0123456789",
#         "email_address": "max.mustermann@example.com",
#         "quantity_of_children": 2,
#         "quantity_of_people_moving_in": 4,
#         "additional_notes": "We are a quiet and responsible family looking for a suitable place to live."
#     }

#     listing_info = {
#         "Title": "++ Sehr helle 2-Zimmer-Wohnung im grünen Wandsbek ++",
#         "City": "Hamburg",
#         "Postal Code": 22041,
#         "District": "Wandsbek",
#         "Kaltmiete": "549 €",
#         "Space": "47 m²",
#         "Deposit": "1647,00 €",
#         "Rooms": 2,
#         "Extra costs": "140 €",
#         "Heating costs": "Heizkosten in Nebenkosten enthalten",
#         "Total cost": "689 €"
#     }"""


