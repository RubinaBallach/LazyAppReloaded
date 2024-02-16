
import openai
from tqdm import tqdm
import time
from dotenv import load_dotenv
import tiktoken
import fitz  # You forgot to import fitz

class ApplicationLetterGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    @staticmethod
    def text_to_pdf(file_path):  #fix the name
        try:
            pdf_document = fitz.open(file_path)
            text_content = ""

            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text_content += page.get_text()

            return text_content
        except Exception as e:
            # Handle exceptions such as API errors
            print(f"Error in extract_cv_info: {e}")
            return None
        
        """
        comment the code"""

    def extract_cv_info(self, prompt, text_to_process):
        #openai.api_key = api_key
        
        try:
            # Make a request to the API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a sophisticated assistant designed to excel in CV analysis for job applications. Take the CV and the prompt to meticulously gather and present the most relevant information."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": text_to_process}
                ]
            )

            return response["choices"][0]['message']['content'].strip()
        
        except Exception as e:
            # Handle exceptions such as API errors
            print(f"Error in extract_cv_info: {e}")
            return None


    
    @staticmethod
    def relevant_job_info(api_key, prompt, text_to_process):  # Added @staticmethod decorator
        openai.api_key = api_key

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a sophisticated assistant designed to excel in job description analysis. Your expertise lies in extracting key details like required skills, qualifications, responsibilities, and any other relevant information. You take a provided job description and a prompt, aiming to meticulously gather and present the most pertinent details."},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": text_to_process}
            ]
        )

        return response['choices'][0]['message']['content'].strip()

    @staticmethod
    def count_tokens(text):
        encoding = tiktoken.encoding_for_model("gpt-4")
        num_tokens = len(encoding.encode(text))
        token_usage_costs = num_tokens / 1000 * 0.02  # Adjust the price per token as needed
        return num_tokens, token_usage_costs

    def generate_application_letter(self, cv_text, job_description):
        # Calculate token usage and costs for CV and job description
        cv_tokens, cv_token_costs = self.count_tokens(cv_text)
        job_tokens, job_token_costs = self.count_tokens(job_description)
    
        # Calculate total token count and costs
        total_tokens = cv_tokens + job_tokens
        total_token_costs = cv_token_costs + job_token_costs
    
        # Create a prompt using CV and job description
        prompt = f"Generate an application letter based on the following CV and job description:\n\nCV:\n{cv_text}\n\nJob Description:\n{job_description}\n\nApplication Letter:"
    
        # Initialize progress bar
        pbar = tqdm(total=1, desc="API Call", unit="request")
    
        start_time = time.time()

        # Make a request to the API using v1/chat/completions
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant that helps users generate application letters."},
                {"role": "user", "content": prompt}
            ]
        )

        # Check the status of the API call
        while 'status' in response and response['status'] == 'in_progress':
            time.sleep(1)  # Adjust the interval as needed
            response = openai.Completion.retrieve(response['id'])

        end_time = time.time()

        # Update progress bar
        pbar.update(1)
        pbar.close()

        # Calculate time consumed
        elapsed_time = end_time - start_time
        print(f"\nTime Consumed: {elapsed_time:.2f} seconds")

        # Format the output
        generated_letter = response['choices'][0]['message']['content'].strip()
        output = (
            f"\nGenerated Application Letter:\n{generated_letter}\n"
            f"\nTotal Token Usage: {total_tokens} tokens, Total Cost: ${total_token_costs:.5f}\n"
            f"Token Usage for CV: {cv_tokens} tokens, Cost: ${cv_token_costs:.5f}\n"
            f"Token Usage for Job Description: {job_tokens} tokens, Cost: ${job_token_costs:.5f}"
        )

        print(output)

if __name__ == "__main__":
    api_key = ""  # Replace with your actual OpenAI API key
    generator = ApplicationLetterGenerator(api_key)

    # Example usage
    cv_text = generator.text_to_pdf("/home/user/Documents/DCI_CODE/LAZY/LAZY2024/lazzy skizzen/EN CV_AlexanderSimakov.pdf")  # Provide the correct path

    # Read job description from a text file
    job_description_file_path = "/home/user/Documents/DCI_CODE/LAZY/LAZY2024/lazzy skizzen/job_string.txt"  # Provide the correct path
    with open(job_description_file_path, 'r', encoding='utf-8') as file:
        job_description = file.read()

    if cv_text is not None:
        print("Extracted CV Text:")
        print(cv_text)

        prompt = "Your prompt here"
        relevant_job_info = generator.relevant_job_info(api_key, prompt, job_description)
        print(f"Processed Job Information:\n{relevant_job_info}")

        generator.generate_application_letter(cv_text, relevant_job_info)
    else:
        print("Failed to extract text from the CV.")


