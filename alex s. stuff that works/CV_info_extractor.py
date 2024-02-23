from openai import OpenAI

client = OpenAI(api_key=api_key)
from tqdm import tqdm
import time
import os
from dotenv import load_dotenv

def process_text(api_key, prompt, text_to_process):
    
    # Start the timer
    start_time = time.time()

    # Make a request to the API
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a sophisticated assistant designed to excel in CV analysis for job applications. Take the CV and the prompt to meticulously gather and present the most relevant information."},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": text_to_process}
    ])

    # Stop the timer
    end_time = time.time()
    elapsed_time = end_time - start_time

    return response.choices[0].message.content.strip(), elapsed_time


if __name__ == "__main__":
    # Example usage
    load_dotenv()
    your_api_key = os.getenv("OPENAI_API_KEY")
    your_prompt = "Extract from the CV: contact information, technical skills,languages including proficiency level, education, work experience in years(extract relevant keywords from the job description that highlight important skills), projects with short description."

    your_text_to_process = """Extracted CV Text:
Extracted CV Text:
Technologies: HTML & CSS,
Python, OOP
Frameworks: Django
Version controls: Git
Databases: Relational
Database Management
System (RDBMS) & SQL,
PostgreSQL
GUI: Tkinter, PyQT
Others: Agile Development,
Project Management
+49 172 232 6750
a.simakov.hh@gmail.com
linkedin.com/in/alex-simakov
Buschrosenweg 24, 22177 HH
C o n t a c t
S k i l l s  
As a Python developer, my
goal is to leverage my
expertise in Python
programming, problem-
solving and software
development to contribute
effectively to a dynamic
team. I am eager to apply
my skills in creating
efficient, scalable, and
high-quality solutions that
meet business needs and
enhance the user
experience.
P r o f i l e
S o u n d  E n g i n e e r ,  T e c h n o l o g y  G r o u p ,  
O d e s s a / K i e v ,  U k r a i n e  
( 0 7 . 2 0 1 8 - 0 2 . 2 0 2 2  f u l l - t i m e / f r e e l a n c e )
Design, assembly, configuration and tuning of high-end sound systems
at events in leading clubs across the country and multi-day festivals,
as well as on-site supervision during the events and collaboration
within larger teams.
E d u c a t i o n
E x p e r i e n c e
Alexander Simakov
P y t h o n  D e v e l o p e r
G y m n a s i u m  O s t e r b e k ,  
H a m b u r g ( 0 8 . 2 0 1 3 - 0 7 . 2 0 1 4 )
Secondary School Diploma
S a l e s  M a n a g e r ,  M M A  H a m b u r g
( 0 8 . 2 0 1 5 - 0 1 . 2 0 1 6 )
Medical Equipment Distribution
Github.com/OdessaHH
S e c o n d a r y  S c h o o l  1 9 ,  
O d e s s a ,  U k r a i n e ( 0 9 . 2 0 1 6 - 0 5 . 2 0 1 7 )
High School Diploma
D C I  C a r e e r  I n s t i t u t e ,  
B e r l i n ( 0 7 . 2 0 2 2 - 0 5 . 2 0 2 4 )
P y t h o n  B a c k e n d  P r o g r a m m i n g
Accomplishing a one-year-full-time training including Python Basics,
Databases, Django Framework, APIs & Cloud Services
Completing multiple small and one final large practical project to
practice programming skills
Completing various Soft-Skill trainings on topics, e.g. Intercultural
Communication, Agile Projectmanagement and SCRUM
S t a g e  M a n a g e r ,  L e  P o n a n t  C r u i s e s
( 0 2 . 2 0 2 0 - 0 4 . 2 0 2 0 )
Responsible for media, sound, and lighting technology in
entertainment on the cruise ship.
S a l e s  M a n a g e r ,  “ P o r t s  o f  U k r a i n e ”  M a g a z i n e ,
O d e s s a ,  U k r a i n e ( 0 9 . 2 0 2 0 - 0 2 . 2 0 2 1 )
Sales of advertisements and other media products
P r o j e c t s
L a z y  P r o j e c t :  A I  C o v e r  L e t t e r  G e n e r a t o r
https://github.com/OdessaHH/LazyApp
S i x S e n s e :  M u s i c  s o r t i n g  t o o l
https://github.com/OdessaHH/6ix-sense
L a n g u a g e s  
German: Native
Russian: Native
English: Advanced
Ukrainian: Advanced
T u t o r ,  D C I  C a r e e r  I n s t i t u t e
( 0 9 . 2 0 2 3 - p r e s e n t )
guiding and supporting students in mastering programming concepts
through one-on-one and group sessions, tailored lesson plans, and
hands-on coding exercises. """
# Set up progress bar
    with tqdm(total=1, desc="Processing", unit="CV") as pbar:
        processed_output, elapsed_time = process_text(your_api_key, your_prompt, your_text_to_process)
        pbar.update(1)

    print("Processed Output:")
    print(processed_output)

    print(f"\nTime taken: {elapsed_time:.2f} seconds")