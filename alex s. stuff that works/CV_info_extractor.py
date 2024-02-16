import openai
from tqdm import tqdm
import time
import os
from dotenv import load_dotenv

def process_text(api_key, prompt, text_to_process):
    openai.api_key = api_key
    
    # Start the timer
    start_time = time.time()

    # Make a request to the API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a sophisticated assistant designed to excel in CV analysis for job applications. Take the CV and the prompt to meticulously gather and present the most relevant information."},
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
    your_prompt = "Extract from the CV: contact information, technical skills,languages including proficiency level, education, work experience in years(extract relevant keywords from the job description that highlight important skills), projects with short description."

    your_text_to_process = """Extracted CV Text:
Jana Müller
P Y T H O N  B A C K E N D  D E V E L O P E R
+ 49 176 123 45 678
jana.mueller@example.com
Musterstraße. 53, 10315 Berlin
Technologies
Python
HTML & CSS
Object-Oriented
Programming
(OOP)
CI/CD
REST API
Amazon Web
Services (AWS)
Frameworks
Django
Flask
Version Controls
Git
A B O U T  M E
L A N G U A G E S
S K I L L S
E D U C A T I O N
DCI Digital Career Institute GmbH, Berlin (05/2023 - 03/2024)
PYTHON BACKEND PROGRAMMING
Accomplishing a one-year-full-time training including Python
Basics, Databases, Django Framework, APIs & Cloud Services
Completing multiple small and one final large practical project to
practice programming skills
Completing various Soft-Skill trainings on topics, e.g. Intercultural
Communication & Agile Projectmanagement
100-DAYS OF CODE: PYTHON PRO BOOTCAMP
JR. BUYER / BUYER, WOMEN’S FOOTWEAR MODERN
Python Developer graduating from a 
nine-months intense training in 
Backend Programming in March 2024. 
Seeking a position to apply experience
from background in E-Commerce,
datadriven Buying & Product Development
and Backend Programming with the
opportunity to grow my skillset and deliver
solution-oriented approaches.
Udemy :  The App Brewery | Dr. Angela Yu (10/2023 - 02/2024)
Learning Python Basics, Databases, APIs, Webscraping, Version
Control and GUI Basics
MASTER’S PROGRAMME: ART HISTORY 
Freie Universität Berlin (10/2008 - 03/2015 | without diploma)
BACHELOR’S PROGRAMME: ART HISTORY | MEDIA &
COMMUNICATION SCIENCE
Heinrich-Heine-Universität Düsseldorf (10/2005 - 04/2008)
Degree: Bachelor of Arts (final mark : 1.4)
W O R K  E X P E R I E N C E
Zalando SE, Berlin (12/2019 - 01/2023)
Datadriven independent purchasing of a broad brand portfolio
incl. negotiation of purchasing conditions
Analysing KPIs, product related Data, Trends and Competitors,
adapting results to presentable formats for internal and external
stakeholders
Collaborating with various internal departments on topics incl.
marketing, platform business and software development
Onboarding and Mentoring of more junior colleagues
PURCHASING ASSISTANT / ASSISTANT BUYER, 
PRIVATE LABEL WOMEN’S FOOTWEAR
zLabels GmbH/Zalando SE , Berlin (08/2015 - 11/2019)
Databases
Relational
Database
Management
System
(RDBMS)
SQL &
PostgreSQL
GUI
Tkinter, PyQt
Others
Agile
Development
Project
Management
TDD
C O N T A C T
German :  
English :  
French : 
Italian : 
Dutch : 
Latin : 
Native Speaker
Professional proficiency (C2)
Conversational (B2)
Pre-intermediate (A2)
Basic (A1)
Latin proficiency certificate
github.com/jamue
Developing products for private label collections and monitoring
relevant sales data and KPIs
Managing communication between an international supplier base
and internal departments 
linkedin.com/in/jana-musterfrau
R E L E V A N T  P R O J E C T S
Practical Module Python Backend Programming (08/2023)
LazyApp
Streamlining application processes utilizing AI
Functional python application with graphical user interface 
Managing a small project in a group of four based on Agile
Methodology
Skills : Python | PyQt | OOP | Agile Projectmanagement
W O R K  E X P E R I E N C E
(continued)
INTERN / PROJECT-BASED EMPLOYEE, LOCAL MARKETING
IKEA Deutschland GmbH & Co. KG , Berlin (08/2012 - 08/2013)
Maintaining local websites  and creating email newsletters for all
four Berlin IKEA Stores
Preparing  online reports ( e.g. on newsletter performance)
Designing and Wording various media (in-store/image brochures) """
# Set up progress bar
    with tqdm(total=1, desc="Processing", unit="CV") as pbar:
        processed_output, elapsed_time = process_text(your_api_key, your_prompt, your_text_to_process)
        pbar.update(1)

    print("Processed Output:")
    print(processed_output)

    print(f"\nTime taken: {elapsed_time:.2f} seconds")