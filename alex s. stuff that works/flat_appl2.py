import openai
import time
from datetime import datetime

class FlatApplicationLetter:
    def __init__(self, listing_info, full_name, date_of_birth, current_address, marital_status, current_occupation,
                 monthly_income, stable_income_available, guarantee_available, clean_schufa_report, references_available,
                 long_term_leasing_desire, quiet_and_tidy_tenant, pets, phone_number, email_address,
                 quantity_of_children, quantity_of_people_moving_in, additional_notes):
        self.listing_info = listing_info
        self.full_name = full_name
        self.date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        self.current_address = current_address
        self.marital_status = marital_status
        self.current_occupation = current_occupation
        self.monthly_income = monthly_income
        self.stable_income_available = stable_income_available
        self.guarantee_available = guarantee_available
        self.clean_schufa_report = clean_schufa_report
        self.references_available = references_available
        self.long_term_leasing_desire = long_term_leasing_desire
        self.quiet_and_tidy_tenant = quiet_and_tidy_tenant
        self.pets = pets
        self.phone_number = phone_number
        self.email_address = email_address
        self.quantity_of_children = quantity_of_children
        self.quantity_of_people_moving_in = quantity_of_people_moving_in
        self.additional_notes = additional_notes

    def generate_flat_application_letter(self):
        prompt = f"""
Schreibe eine Bewerbung für die Wohnung. Die Wohnung ist in {self.listing_info["City"]} und hat {self.listing_info["Rooms"]} Zimmer. Die Kaltmiete beträgt {self.listing_info["Kaltmiete"]} und die Wohnfläche beträgt {self.listing_info["Space"]}. Die Wohnung befindet sich in {self.listing_info["District"]} und hat eine Gesamtmiete von {self.listing_info["Total cost"]}. Wenn du etwas über {self.listing_info["District"]} in {self.listing_info["City"]} weißt, begründe warum du dort wohnen möchtest.

**Persönliche Informationen:**
- Vollständiger Name: {self.full_name}
- Geburtsdatum: {self.date_of_birth}
- Aktuelle Adresse: {self.current_address}
- Familienstand: {self.marital_status}
- Aktueller Beruf: {self.current_occupation}
- Monatliches Einkommen: {self.monthly_income} €
- Stabiles Einkommen verfügbar: {self.stable_income_available}
- Garantie verfügbar: {self.guarantee_available} (wenn ja, bitte angeben, ansonsten nicht)
- Saubere Schufa-Auskunft: {self.clean_schufa_report} (wenn ja, bitte angeben, ansonsten nicht)
- Referenzen von früheren Vermietern verfügbar: {self.references_available} (wenn ja, bitte angeben, ansonsten nicht)
- Wunsch nach einer langfristigen Mietbeziehung: {self.long_term_leasing_desire}
- Ruhiger und ordentlicher Mieter: {self.quiet_and_tidy_tenant} (wenn ja, bitte angeben, ansonsten nicht)
- Haustiere: {self.pets} (wenn ja, bitte angeben, ansonsten nicht)
- Telefonnummer: {self.phone_number}
- E-Mail-Adresse: {self.email_address}
- Anzahl der Kinder: {self.quantity_of_children} (wenn ja, bitte angeben, ansonsten schreib "keine")
- Anzahl der Personen, die einziehen: {self.quantity_of_people_moving_in} (anhand dessen schreibst du in ich oder wir Form)
- Zusätzliche Notizen: {self.additional_notes} (berücksichtige diese Notizen in der Bewerbung)

Die Bewerbung sollte in deutscher Sprache generiert werden.

hier ein Beispiel für die Bewerbung, solchen Format soll es haben, aber berücksichtige die oben genannten Informationen und füge die an richtigen Stellen ein:

{self.full_name}
{self.current_address}
Telefon: {self.phone_number}
E-Mail: {self.email_address}

Vermietungsagentur
z. H. Zuständige Person
Adresszusatz

<Datum>

Bewerbung für die {self.listing_info["Rooms"]}-Zimmer-Wohnung in {self.listing_info["City"]}

Sehr geehrte Damen und Herren,

{ "ich" if self.quantity_of_people_moving_in == 1 else f"wir, Familie {self.full_name}," } möchten uns als Bewerber für die oben genannte Wohnung vorstellen. { "Ich bin" if self.quantity_of_people_moving_in == 1 else "Wir sind" } seit {self.current_occupation} berufstätig. { "Mein" if self.quantity_of_people_moving_in == 1 else "Unser" } gemeinsames Einkommen beträgt monatlich {self.monthly_income} € brutto. Gehaltsabrechnungen und Arbeitgeberbescheinigungen haben wir beigefügt.

{f'Wir haben {self.quantity_of_children} Kinder. {{...expandiere hier...}} Jetzt, da die Kinder größer sind und { "beide" if self.quantity_of_children > 1 else "ein" } eigenes Zimmer bekommen sollen, reicht der Platz in unserer derzeitigen Wohnung nicht mehr aus.' if self.quantity_of_children else ''}

Ihre ausgeschriebene {self.listing_info["Rooms"]}-Zimmer-Wohnung entspricht in Größe und Zuschnitt genau unseren Vorstellungen. {f' {self.additional_notes}.' if self.additional_notes else ''}

Wir freuen uns auf die Möglichkeit, die Wohnung persönlich zu besichtigen, und auf ein persönliches Gespräch.

Mit freundlichen Grüßen,
{self.full_name}

Anlagen:
- Gehaltsabrechnungen
- SCHUFA-Auskunft
- {f'Referenzen früherer Vermieter' if self.references_available else ''}
- {f'Nachweis über Garantie' if self.guarantee_available else ''}
"""


        start_time = time.time()

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Du bist ein KI Assistent, der eine Bewerbung für eine Wohnung schreibt.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"\nTime Consumed: {elapsed_time:.2f} seconds")

        cover_letter = response["choices"][0]["message"]["content"].strip()
        print(cover_letter)
        return cover_letter


if __name__ == "__main__":
    # Replace "YOUR_API_KEY" with your actual OpenAI API key
    openai.api_key = "

    # Example usage
    user_criteria = {
    "full_name": "Max Mustermann",
    "date_of_birth": "1990-01-01",
    "current_address": "Musterstraße 1",
    "marital_status": "Single",
    "current_occupation": "Software Developer",
    "monthly_income": 3000,
    "stable_income_available": True,
    "guarantee_available": False,
    "clean_schufa_report": True,
    "references_available": True,
    "long_term_leasing_desire": True,
    "quiet_and_tidy_tenant": True,
    "pets": False,
    "phone_number": "0123456789",
    "email_address": "max.mustermann@example.com",
    "quantity_of_children": 2,
    "quantity_of_people_moving_in": 4,
    "additional_notes": "We are a quiet and responsible family looking for a suitable place to live."
}

    listing_info = {
    "Title": "++ Sehr helle 2-Zimmer-Wohnung im grünen Wandsbek ++",
    "City": "Hamburg",
    "Postal Code": 22041,
    "District": "Wandsbek",
    "Kaltmiete": "549 €",
    "Space": "47 m²",
    "Deposit": "1647,00 €",
    "Rooms": 2,
    "Extra costs": "140 €",
    "Heating costs": "Heizkosten in Nebenkosten enthalten",
    "Total cost": "689 €"
}
    generator = FlatApplicationLetter(listing_info=listing_info, **user_criteria)
    generated_flat_letter = generator.generate_flat_application_letter()
