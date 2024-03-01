from bs4 import BeautifulSoup
from selenium import webdriver
import re
import requests


class FlatAdImporter:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }

    def parse_immowelt(self):
        website = requests.get(immowelt_url, headers= self.headers)
        soup = BeautifulSoup(website.text, "html.parser")

        #Extracting the title of the flat description
        title_element = soup.find("h1", class_="ng-star-inserted")
        title = title_element.text.strip() if title_element else None
        print("Title:", title)

        # Extracting City, Postal Code and District
        address_element = soup.find("span", {"data-cy": "address-city"})
        if address_element:
            address_text = address_element.text.strip()
            address_match = re.match(r"(\d{5})\s*([^\(]+)\s*\(([^)]+)\)", address_text)
            if address_match:
                postal_code = address_match.group(1)
                city = address_match.group(2).strip()
                district = address_match.group(3).strip()
                print("City:", city)
                print("Postal Code:", postal_code)
                print("District:", district)

        #Extracting the cost without extra costs and heating costs
        kaltmiete_element = soup.find("strong", class_="ng-star-inserted")
        kaltmiete = (
            kaltmiete_element.text.strip()
            if kaltmiete_element
            else "Kaltmiete not found"
        )
        print("Kaltmiete:", kaltmiete)

        #Extracting the space of the flat
        space_element = soup.find("span", class_="has-font-300")  # fläche
        space = space_element.text.strip() if space_element else "Space not found"
        print("Space:", space)

        #Extracting the deposit of the flat
        deposit_element = soup.find("p", class_="card-content")
        deposit_value = deposit_element.text.strip() if deposit_element else None

        if deposit_value:
            deposit = f"{deposit_value} €"
            print("Deposit:", deposit)
        else:
            print("Deposit not found")

        #Extracting the quantity of rooms of the flat
        rooms_element = soup.find("span", class_="has-font-300")
        for _ in range(7):
            rooms_element = rooms_element.next_element
        rooms = rooms_element.text.strip() if rooms_element else "rooms not found"
        print("Rooms:", rooms)  # anzahl zimmer

        #Extracting the extra costs 
        extra_costs_element = soup.find(
            "sd-cell-col", class_="cell__col is-pulled-right"
        )
        for _ in range(13):
            extra_costs_element = extra_costs_element.next_element

        if extra_costs_element:
            extra_costs_value = extra_costs_element.text.strip()
            print("Extra costs:", extra_costs_value)
        else:
            print("Cost not found")

        #Extracting the heating costs
        heating_costs_element = soup.find(
            "sd-cell-col", class_="cell__col is-pulled-right"
        )
        for _ in range(18):
            heating_costs_element = heating_costs_element.next_element

        if heating_costs_element:
            heating_costs_value = heating_costs_element.text.strip()
            print("Heating costs:", heating_costs_value)
        else:
            print("Cost not found")

        #Extracting the total cost
        total_cost_element = soup.find(
            "sd-cell-col", class_="cell__col is-pulled-right"
        )
        for _ in range(35):
            total_cost_element = total_cost_element.next_element

        if total_cost_element:
            total_cost_value = total_cost_element.text.strip()
            print("Total cost:", total_cost_value)

        #Extracting the data of the landlord
        landlord_company_element = soup.find('p', class_='offerer').get_text(strip=True)     
        person_in_charge_element = soup.find('p', class_='is-bold').get_text(strip=True)
        company_address_element =  soup.find('p', {'data-cy': 'offerer-address'}).get_text(strip=True)

        print("Landlord:", landlord_company_element)
        print("Person in charge:", person_in_charge_element)
        print("Company address:", company_address_element)



        return {
            "Job title": title,
            "City": city,
            "Postal Code": postal_code,
            "District": district,
            "Kaltmiete": kaltmiete,
            "Space": space,
            "Deposit": deposit,
            "Rooms": rooms,
            "Extra costs": extra_costs_value,
            "Heating costs": heating_costs_value,
            "Total cost": total_cost_value,
            "Landlord (Company)": landlord_company_element,
            "Person in charge": person_in_charge_element,
            "Company address": company_address_element
        }
    # available_element = "" # could not fix the availability of the flat
    

"""
#testing 
#immowelt_url = "https://www.immowelt.de/expose/2dxcn5j"
#immowelt_url = "https://www.immowelt.de/expose/2dvct5l" #privater anbieter
immowelt_url = "https://www.immowelt.de/expose/2d4j55l"
flat_importer = FlatAdImporter(immowelt_url)
flat_importer.parse_immowelt()
"""