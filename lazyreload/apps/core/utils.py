
import openai
import time
import os
from dotenv import load_dotenv
import fitz

# import tiktoken

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


class CVTextExtractor:
    def __init__(self, api_key, file_path):
        self.api_key = api_key
        openai.api_key = api_key
        self.filepath = file_path
        self.cv_token_costs = 0
        self.text_content = ""  # Initialize as an empty string


    def pdf_to_text(self):
        """
        Extracts text from the CV in PDF format to text format.
        """
        try:
            pdf_document = fitz.open(self.filepath)

            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text_content += page.get_text()

            return text_content
        except Exception as e:
            # Handle exceptions such as API errors
            print(f"Error in extract_cv_info: {e}")
            return None

    # Double check which text the token counter needs
    # def count_tokens(text):
    #     encoding = tiktoken.encoding_for_model("gpt-4")
    #     num_tokens = len(encoding.encode(text))
    #     token_usage_costs = num_tokens / 1000 * 0.02  # Adjust the price per token as needed
    #     return num_tokens, token_usage_costs

    def extract_cv_info(self):
        """
        Takes text from CV PDF and returns the most relevant information utilizing openai's GPT-4 model.
        """
        # # Count tokens and token usage costs for the CV
        # self.cv_token_costs = self.count_tokens(cv_text)

        try:
            # Make a request to the API
            prompt = "Take the CV and meticulously gather and present the most relevant information."
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a sophisticated assistant designed to excel in CV analysis for job applications.",
                    },
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": self.text_content},
                ],
            )
            cv_extract = response["choices"][0]["message"]["content"].strip()
            return cv_extract

        except Exception as e:
            # Handle exceptions such as API errors
            return f"Error in extract_cv_info: {e}"


class CoverLetterGenerator:
    def __init__(self, api_key, job_description, cv_extract):
        self.api_key = api_key
        openai.api_key = api_key
        self.job_description = job_description
        self.cv_extract = cv_extract
        self.job_extract = self.relevant_job_info()

    # def count_tokens(text):
    #     encoding = tiktoken.encoding_for_model("gpt-4")
    #     num_tokens = len(encoding.encode(text))
    #     token_usage_costs = num_tokens / 1000 * 0.02  # Adjust the price per token as needed
    #     return num_tokens, token_usage_costs

    def relevant_job_info(self):
        """
        Takes job description and extracts the most relevant information utilizing openai's GPT-4 model.
        """
        openai.api_key = self.api_key
        prompt = "You take a provided job description and a prompt, aiming to meticulously gather and present the most pertinent details."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a sophisticated assistant designed to excel in job description analysis. Your expertise is extracting key details like required skills, qualifications, responsibilities, and any other relevant information. ",
                },
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": self.job_description},
            ],
        )
        self.job_extract = response["choices"][0]["message"]["content"].strip()
        return self.job_extract

    def generate_application_letter(self):
        """
        Takes all user information, cv and job extracts and generates an application letter using openai's GPT-4 model.
        """
        # Calculate token usage and costs for CV and job description
        # job_tokens, job_token_costs = self.count_tokens(job_description)
        # # Calculate total token count and costs
        # total_tokens = cv_tokens + job_tokens
        # total_token_costs = cv_token_costs + job_token_costs

        # Create a prompt using CV and job description
        prompt = f"""Generate an application letter based on the following CV and job description:
                    CV:\n{self.cv_extract}\n\nJob Description:\n{self.job_extract}\n\nApplication Letter:"""

        start_time = time.time()

        # Make a request to the API using v1/chat/completions
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that helps users generate application letters.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        # Calculate time consumed
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(
            f"\nTime Consumed: {elapsed_time:.2f} seconds"
        )  # Testing puposes remove in production

        # Format the output
        cover_letter = response["choices"][0]["message"]["content"].strip()
        # output = (
        #     f"\nGenerated Application Letter:\n{generated_letter}\n"
        #     # f"\nTotal Token Usage: {total_tokens} tokens, Total Cost: ${total_token_costs:.5f}\n"
        #     # f"Token Usage for CV: {cv_tokens} tokens, Cost: ${cv_token_costs:.5f}\n"
        #     # f"Token Usage for Job Description: {job_tokens} tokens, Cost: ${job_token_costs:.5f}"
        # )

        print(cover_letter)
        return cover_letter


if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
  # update the api key in env file
    generator = CVTextExtractor(api_key, "/home/user/Documents/DCI_CODE/LAZY/LAZY2024/lazzy skizzen/EN CV_AlexanderSimakov.pdf")

    # Example usage
    cv_text = generator.extract_cv_info()
    print(cv_text)
    # )  # Provide the correct path stored in db

    # # Read job description from a text file
    
    # with open(job_description_file_path, "r", encoding="utf-8") as file:
    #     job_description = file.read()

    # if cv_text is not None:
    #     print("Extracted CV Text:")
    #     print(cv_text)

    #     prompt = "Your prompt here"  # where will this come from?
    #     relevant_job_info = generator.relevant_job_info(
    #         api_key, prompt, job_description
    #     )
    #     print(f"Processed Job Information:\n{relevant_job_info}")

    #     generator.generate_application_letter(cv_text, relevant_job_info)
    # else:
    #     print("Failed to extract text from the CV.")
