from openai import OpenAI
import time
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader

# All AI supported functionalities are implemented in this file


class CVTextExtractor:
    def __init__(self, OPENAI_API_KEY, file_path):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.filepath = file_path
        self.text_content = self.pdf_to_text()

    def pdf_to_text(self):
        """
        Extracts text from the CV in PDF format to text format.
        """
        try:
            reader = PdfReader(self.filepath)
            self.text = ""
            for page in reader.pages:
                self.text += page.extract_text()
            return self.text
      
        except Exception as e:
            # Handle exceptions such as API errors
            print(f"Error in extract_cv_info: {e}")
            return None

    def extract_cv_info(self):
        """
        Takes text from CV PDF and returns the most relevant information utilizing openai's GPT-4 model.
        """

        try:
            # Make a request to the API
            prompt = "Take the CV and meticulously gather and present the most relevant information."
            response = self.client.chat.completions.create(model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a sophisticated assistant designed to excel in CV analysis for job applications.",
                },
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": self.text_content},
            ])
            cv_extract = response.choices[0].message.content.strip()
            return cv_extract

        except Exception as e:
            # Handle exceptions such as API errors
            return f"Error in extract_cv_info: {e}"

# CV extract from Database, Job Description from Database
class CoverLetterGenerator:
    def __init__(self, api_key, job_description, cv_extract):
        self.client = OpenAI(api_key=api_key)
        self.job_description = job_description
        self.cv_extract = cv_extract
        self.job_extract = self.relevant_job_info()

    def relevant_job_info(self):
        """
        Takes job description and extracts the most relevant information utilizing openai's GPT-4 model.
        """
        prompt = "You take a provided job description and a prompt, aiming to meticulously gather and present the most pertinent details."
        response = self.client.chat.completions.create(model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a sophisticated assistant designed to excel in job description analysis. Your expertise is extracting key details like required skills, qualifications, responsibilities, and any other relevant information. ",
            },
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": self.job_description},
        ])
        self.job_extract = response.choices[0].message.content.strip()
        return self.job_extract

    def generate_application_letter(self):
        """
        Takes all user information, cv and job extracts and generates an application letter using openai's GPT-4 model.
        """
        # Create a prompt using CV and job description
        prompt = f"""Generate an application letter based on the following CV and job description:
                    CV:\n{self.cv_extract}\n\nJob Description:\n{self.job_extract}\n\nApplication Letter:"""

        start_time = time.time()

        # Make a request to the API using v1/chat/completions
        response = self.client.chat.completions.create(model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant that helps users generate application letters.",
            },
            {"role": "user", "content": prompt},
        ])

        # Calculate time consumed
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(
            f"\nTime Consumed: {elapsed_time:.2f} seconds"
        )  # Testing puposes remove in production

        # Format the output
        cover_letter = response.choices[0].message.content.strip()

        print(cover_letter)
        return cover_letter


if __name__ == "__main__":
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    generator = CVTextExtractor(OPENAI_API_KEY,
                                 "lazyreload/media/cvs/TestCV_Lazy_App.pdf")
    print(generator.extract_cv_info())

    # # Example usage
    # cv_text = generator.extract_cv_info()
    # print(cv_text)

