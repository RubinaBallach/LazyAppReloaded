from openai import OpenAI

client = OpenAI(api_key=api_key)
from tqdm import tqdm
import time
import os
from dotenv import load_dotenv
import tiktoken

def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-4")
    num_tokens = len(encoding.encode(text))
    token_usage_costs = num_tokens / 1000 * 0.02  # Adjust the price per token as needed
    return num_tokens, token_usage_costs

def generate_application_letter(api_key, cv_text, job_description):
    
    # Calculate token usage and costs for CV and job description
    cv_tokens, cv_token_costs = count_tokens(cv_text)
    job_tokens, job_token_costs = count_tokens(job_description)
    
    # Calculate total token count and costs
    total_tokens = cv_tokens + job_tokens
    total_token_costs = cv_token_costs + job_token_costs
    
    # Create a prompt using CV and job description
    prompt = f"Generate an application letter based on the following CV and job description:\n\nCV:\n{cv_text}\n\nJob Description:\n{job_description}\n\nApplication Letter:"
    
    # Initialize progress bar
    pbar = tqdm(total=1, desc="API Call", unit="request")
    
    start_time = time.time()

    # Make a request to the API using v1/chat/completions
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an AI assistant that helps users generate application letters."},
        {"role": "user", "content": prompt}
    ])

    # Check the status of the API call
    while 'status' in response and response.status == 'in_progress':
        time.sleep(1)  # Adjust the interval as needed
        response = client.completions.retrieve(response.id)

    end_time = time.time()

    # Update progress bar
    pbar.update(1)
    pbar.close()

    # Calculate time consumed
    elapsed_time = end_time - start_time
    print(f"\nTime Consumed: {elapsed_time:.2f} seconds")

    # Format the output
    generated_letter = response.choices[0].message.content.strip()
    output = (
        f"\nGenerated Application Letter:\n{generated_letter}\n"
        f"\nTotal Token Usage: {total_tokens} tokens, Total Cost: ${total_token_costs:.5f}\n"
        f"Token Usage for CV: {cv_tokens} tokens, Cost: ${cv_token_costs:.5f}\n"
        f"Token Usage for Job Description: {job_tokens} tokens, Cost: ${job_token_costs:.5f}"
    )

    print(output)

if __name__ == "__main__":
    # Example usage
    load_dotenv()
    your_api_key = os.getenv("API_KEY")
    
    # Sample CV text and job description
    cv_text = """
    Contact Information:
- Name: Jana Müller
- Phone Number: + 49 176 123 45 678
- Email Address: jana.mueller@example.com
- Address: Musterstraße. 53, 10315 Berlin
- Github: github.com/jamue
- LinkedIn: linkedin.com/in/jana-musterfrau

Technical Skills:
- Python, HTML & CSS, Object-Oriented Programming (OOP), REST API, Amazon Web Services (AWS), CI/CD
- Frameworks: Django, Flask
- Version Controls: Git
- Databases: Relational Database Management System (RDBMS), SQL & PostgreSQL
- GUI: Tkinter, PyQt
- Others: Agile Development, Project Management, TDD

Languages:
- German: Native Speaker
- English: Professional proficiency (C2)
- French: Conversational (B2)
- Italian: Pre-intermediate (A2)
- Dutch: Basic (A1)
- Latin: Latin proficiency certificate 

Education:
- DCI Digital Career Institute GmbH, Berlin (PYTHON BACKEND PROGRAMMING): 05/2023 - 03/2024
- Udemy: Python Pro Bootcamp (The App Brewery | Dr. Angela Yu): 10/2023 - 02/2024
- Freie Universität Berlin (MASTER’S PROGRAMME: ART HISTORY): 10/2008 - 03/2015 (without diploma)
- Heinrich-Heine-Universität Düsseldorf (BACHELOR’S PROGRAMME: ART HISTORY | MEDIA & COMMUNICATION SCIENCE): 10/2005 - 04/2008, Degree: Bachelor of Arts (final mark: 1.4)

Work Experience:
- Zalando SE, Berlin (12/2019 - 01/2023): Datadriven independent purchasing, analyzing KPIs, product related data, trends and competitors, and adapting results to presentable formats. Total experience: 4 years
- zLabels GmbH / Zalando SE, Berlin (08/2015 - 11/2019): Developing products for private label collections and monitoring relevant sales data and KPIs. Total experience: 4 years
- IKEA Deutschland GmbH & Co. KG, Berlin (08/2012 - 08/2013): Maintaining local websites and creating email newsletters. Total experience: 1 year.
Total work Experience: 9 years

Relevant Projects:
- Practical Module Python Backend Programming (08/2023): LazyApp, a functional python application with graphical user interface that streamlines application processes utilizing AI. Skills used include Python, PyQt, OOP, and Agile Projectmanagement.
    """
    
    job_description = """
    Job Title: Backend Python Software Developer 

Department or Team: IT team

Main Responsibilities:
- Develop and maintain backend infrastructure
- Interface with external APIs provided by partners
- Develop data pipelines
- Create documentation for all created products
- Ensure that all products are scalable and resilient to failure
- Work with other developers to ensure best practices are followed during development and deployment of new features or products

Qualifications and Skills:
- Proficiency in backend Python and Web development
- Proficiency in Python 3 and generators and list comprehensions
- Familiarity with Python decorators
- Understanding of the concepts of object-oriented design and functional programming
- Experience with Flask or a similar web framework
- Comfortability with SQL, Linux/Bash, Git

Company Information:
Yieldlove is an industry leader in programmatic online advertising, aimed at maximizing revenues for over 700 publishers worldwide. The organization is characterized by a diverse, passionate, and international team. It values flat hierarchies, room for individuality, and flexible working models, including a home office option.

Application process: Applicants must demonstrate their proficiency in English or German and submit their CV, salary expectations, and earliest possible starting date in an informal application.

Work Location: The position is based in Hamburg but remote work is an option.

Working Hours: 
The job entails 40 hours per week with no expected overtime.

Salary and Benefits:
- Competitive salary
- Unlimited work contract with 30 vacation days per year 
- Free HVV Proficard ticket
- Choice of work equipment
- Option to work from home
- Access to a company gym
- Centrally-located office in the HafenCity area
- Free drinks including tea, water, juices, and coffee
- Free beer every Friday and access to various vending machines
- A rooftop terrace
- A video gaming area.
    """
    
    
    # Generate the application letter
    application_letter = generate_application_letter(your_api_key, cv_text, job_description)
    
    print("\nGenerated Application Letter:")
    print(application_letter)

