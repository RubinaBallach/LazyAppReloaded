import openai
from tqdm import tqdm
import time
import os
from dotenv import load_dotenv

def process_job_description(api_key, prompt, text_to_process):
    openai.api_key = api_key
    
    # Start the timer
    start_time = time.time()

    # Make a request to the API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a sophisticated assistant designed to excel in job description analysis. Your expertise lies in extracting key details like required skills, qualifications, responsibilities, and any other relevant information. You take a provided job description and a prompt, aiming to meticulously gather and present the most pertinent details."},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": text_to_process}
        ]
    )

    # Stop the timer
    end_time = time.time()
    elapsed_time = end_time - start_time

    return response['choices'][0]['message']['content'].strip(), elapsed_time

if __name__ == "__main__":
    # Example usage
    load_dotenv()
    your_api_key = os.getenv("API_KEY")
    your_prompt = "Extract the following information from the job description: required skills, qualifications, responsibilities, and any other relevant details. Extract the specific job title and the department or team the role belongs to. Identify the main responsibilities and duties associated with the role. Extract information about the qualifications, skills, and experience required for the job. Identify the key skills and competencies mentioned in the job description. Extract information about the company, its mission, values, and any unique aspects that applicants should be aware of. Look for details about how applicants should apply, including submission instructions, required documents, and deadlines. Extract details about the location of the job, working hours, and any specific working conditions or travel requirements. Identify information about the benefits and perks associated with the role, such as health benefits, retirement plans, or additional incentives. Extract salary details or any information about the compensation package. If provided, extract contact information for the hiring manager or HR representative, which can be useful for applicants with questions."
    your_text_to_process = """Job Description:
    Company Description

Remark: Working with us at Yieldlove requires you to be more or less fluent in English. Anyhow we are happy to receive your application in either English or German.

Yieldlove leads publishers and website operators into the future of programmatic online advertising.

As a market leader in the European ad tech industry, we are able to offer our partners tailored solutions to maximize their revenues and ensure their sustainable economic success. Whether large publishing houses, independent websites or trendy apps: Over 700 publishers worldwide rely on our proprietary technologies and our many years of expertise.

Driving our success is a diverse, passionate, and experienced team from around the world. Our employees are our focus - that's why we strongly believe in flat hierarchies, room for individuality and flexible working models including a home office option.

We are looking for an experienced Backend Python Software Developer (m/f/d) to join our IT team full time in our office in Hamburg or remote. The Backend Python Developer is responsible for developing and maintaining our backend infrastructure. This includes the development of internal systems and working with external APIs, and data pipelines.
Job Description

    Develop and maintain our backend infrastructure
    Interfacing with external APIs provided by our partners
    Develop data pipelines
    Create appropriate documentation for all created products
    Ensure that all products are scalable and resilient to failure
    Work with other developers to ensure best practices are followed during development and deployment of new features or products

Qualifications

    You should be well versed in backend Python and Web development
    You should be proficient in Python 3 and generators and list comprehensions should be your second nature
    Python decorators should also be part of your skill set
    Object oriented design comes naturally to you but you are also aware of the benefits of functional programming
    Experience with Flask or a similar web framework completes your skill
    set
    Furthermore, you should feel comfortable with SQL, Linux/Bash, Git

Additional Information

    Competitive salary
    Unlimited work contract with 30 vacation days/year
    40 working hours per week with no overtime
    HVV Proficard ticket
    Work equipment of your choice
    With us you also have the chance to work from home
    Friendly work atmosphere within an international team; no dress code
    Nice and centrally-located office located in the HafenCity (U-Bahn station Baumwall)
    Free drinks like tea, water, juices and excellent coffee
    Free beer every Friday in the penthouse-lounge
    Instant access to the various vending machines (snacks, ice cream, HelloFreshGO)
    Company gym
    Rooftop terrace
    Video-gaming area

We are an international team and we like to talk to each other. Therefore, you should be more or less fluent in English if you want to work at Yieldlove. We are looking forward to your informal application in German or English including CV, salary expectations and earliest possible starting date.
    """

    # Set up progress bar
    with tqdm(total=1, desc="Processing", unit="Job Description") as pbar:
        processed_output, elapsed_time = process_job_description(your_api_key, your_prompt, your_text_to_process)
        pbar.update(1)

    print("Processed Output:")
    print(processed_output)

    print(f"\nTime taken: {elapsed_time:.2f} seconds")
