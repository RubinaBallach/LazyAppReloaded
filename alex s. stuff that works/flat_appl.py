import openai
import os
import time
import dotenv

class  RentApplicationGenerator:
    def __init__(self, api_key, user_criteria, flat_criteria):
        self.api_key = api_key
        openai.api_key = api_key
        self.user_criteria = user_criteria
        self.flat_criteria = flat_criteria
        #self.flat_extract = self.relevant_flat_info()

    """def relevant_flat_info(self): #maybe i will implement this later
        
        #Takes flat criteria and extracts the most relevant information utilizing openai's GPT-4 model.
        
        openai.api_key = self.api_key
        prompt = "You take provided flat criteria and a prompt, aiming to meticulously gather and present the most pertinent details."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a sophisticated assistant designed to excel in flat criteria analysis. Your expertise is extracting key details like location, space, number of rooms, Kaltmiete, and any other relevant information.",
                },
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": str(self.flat_criteria)},
            ],
        )
        flat_extract = response["choices"][0]["message"]["content"].strip()
        return flat_extract"""

    def generate_application_letter(self):
        """
        Takes all user information, CV and flat extracts, and generates an application letter using openai's GPT-4 model.
        """
        prompt = f"""Generate an application letter based on the following user and flat criteria:
        Generate an application letter for the apartment based on the following information:

        **Personal Information:**
        - Full Name: [Your Name]
        - Date of Birth: [Your Date of Birth]
        - Current Address: [Your Address]
        - Marital Status: [Single/Married/etc.]

        **Professional Information:**
        - Current Occupation: [Your Occupation]
        - Monthly Income: [Your Monthly Income]

        **Financial Stability:**
        - Stable income available.
        - Guarantee available: [Yes/No]
        - Clean Schufa report: [Yes]

        **References:**
        - References from previous landlords available: [Yes/No]

        **Intent to Lease:**
        - Desire for a long-term leasing relationship.

        **Responsibility:**
        - Quiet and tidy tenant.
        - Responsible handling of the apartment.

        **Pets:**
        - Pets: [Yes/No] (if applicable)

        **Contact Information:**
        - Phone Number: [Your Phone Number]
        - Email Address: [Your Email Address]

        [Here could be optional space for additional notes or individual preferences of the applicant.]
        The applicatioon should be generated in german language.
                    User Criteria:\n{self.user_criteria}\n\nFlat Criteria:\n{self.flat_criteria}\n"""

        start_time = time.time()

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that helps users generate application letters for flat application.",
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
    api_key = "API_KEY"
    user_criteria = {
    "Name": "Max Mustermann",
    "Date of Birth": "01/01/1990",
    "Address": "Sample Street 123, 12345 Sample City",
    "Marital Status": "Single",

    "Occupation": "IT Specialist",
    "Monthly Income": 4000.00,

    "Stable Income Available": True,
    "Guarantee Available": False,
    "Clean Schufa Report": True,

    "References from Previous Landlords": True,

    "Desire for Long-Term Lease": True,

    "Quiet and Tidy Tenant": True,
    "Responsible Handling of the Property": True,

    "Pets": False,

    "Phone Number": "+49 123 456789",
    "Email Address": "max.mustermann@example.com"   
    }


    flat_criteria = {
        "Country": "Germany",
        "State": "Hamburg",
        "City": "Hamburg",
        "PropertyType": "Flat",
        "Space": 35,
        "NoOfRooms": 1,
        "Kaltmiete": 470,
        "Kitchen": True
    }

    generator = RentApplicationGenerator(api_key, user_criteria, flat_criteria)
    generated_letter = generator.generate_application_letter()
