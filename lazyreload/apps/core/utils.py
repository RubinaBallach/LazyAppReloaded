
from openai import OpenAI
import time
import os
from dotenv import load_dotenv
from pypdf import PdfReader

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
    def __init__(self, api_key, 
                 job_description, cv_extract, 
                 job_type, salary_expectation, 
                 to_highlight, availability):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.job_description = job_description
        self.cv_extract = cv_extract
        self.job_type = job_type
        self.salary_expectation = salary_expectation
        self.to_highlight = to_highlight
        self.availability = availability

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
        job_extract = response.choices[0].message.content.strip()
        return job_extract

    def generate_cover_letter(self):
        """
        Takes all user information, cv and job description and generates an application letter using openai's GPT-4 model.
        """
        # get job extract from description
        self.job_extract = self.relevant_job_info()
        # Create a prompt using CV and job description
        prompt = f"""
                    Generate an application letter based on the following CV and job description:
                    CV:\n{self.cv_extract}\n\nJob Description:\n{self.job_extract}. 
                    The applicant is looking for a {self.job_type} position 
                    and is avaiable from {self.availability}.

                    Generate application letter in language of Job Description(if job description is in German, letter should be in German).

                    Carefully consider following:
                    - Salary expectation: {self.salary_expectation}
                    - Highlight: {self.to_highlight}
                    
                    Please only consider the most relevant information from the CV and Job Description. Double check to dont make things up.

                    Use the best job applying language and make sure to adapt the wording to the job the user wants to apply for and provide additional information on companies and competitive market salaries. 


                    Do not repeat yourself by starting alamost every sentence with "I am" or "I have". Be creative and use synonyms. It is very importnat

                    Write the letter in a professional and polite manner.
                    
                    The letter should be around 300 words.

                    """
        if self.salary_expectation != 0:
            prompt += f"""The salary expectation is {self.salary_expectation} per year."""
        if self.to_highlight != "": 
            prompt += f"""Highlight the following: {self.to_highlight}"""


        start_time = time.time()

        # Make a request to the API using v1/chat/completions

        response = self.client.chat.completions.create(model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant that helps users generate application letters.ou are a helpful expert for jobsearch and application. You adapt the wording in regards to the job the user wants to apply for and provide additional information on companies",
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

        # print(cover_letter)
        return cover_letter


if __name__ == "__main__":
    load_dotenv()
    # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # generator = CVTextExtractor(OPENAI_API_KEY,
    #                              "lazyreload/media/cvs/TestCV_Lazy_App.pdf")
    # cv_text = generator.extract_cv_info()
    # print(cv_text)
    # cv_text = """NAME: Jana Müller
    # NATIONALITY: German
    # LOCATION: Berlin, Germany
    # CONTACT: + 49 176 123 45 678 | jana.mueller@example.com

    # PROFESSION: Python Backend Developer
    # SKILLS: Python, HTML & CSS, Object-Oriented Programming (OOP), CI/CD, REST API, Amazon Web Services (AWS), Django, Flask, Git, Relational Database Management System (RDBMS), SQL & PostgreSQL, Tkinter, PyQt, Agile Development, and Project Management

    # EDUCATION:
    # - DCI Digital Career Institute GmbH, Berlin (Python Backend Programming) | 05/2023 - 03/2024
    # - Udemy: The App Brewery | Dr. Angela (Python Pro Bootcamp) | 10/2023 - 02/2024
    # - Freie Universität Berlin (Master’s Programme: Art History) | 10/2008 - 03/2015
    # - Heinrich-Heine-Universität Düsseldorf (Bachelor’s in Art History | Media & Communication Science) | 10/2005 - 04/2008

    # WORK EXPERIENCE:
    # - Zalando SE, Berlin (Jr. Buyer / Buyer, Women’s Footwear Modern) | 12/2019 - 01/2023
    # - zLabels GmbH/Zalando SE, Berlin (Purchasing Assistant / Assistant Buyer, Private Label Women’s Footwear) | 08/2015 - 11/2019

    # LANGUAGES: German (Native Speaker), English (C2), French (B2), Italian (A2), Dutch (A1), Latin proficient

    # PERSONAL PROJECTS: Practical Module Python Backend Programming, LazyApp

    # SOCIAL PROFILES: [LinkedIn](https://www.linkedin.com/in/jana-musterfrau), [Github](https://github.com/jamue)

    # Jana is a graduating Python Backend Developer looking for an opportunity to apply her experience from e-Commerce, data-driven buying & product development, and backend programming with a goal to grow her skillset further. She previously held posts at Zalando SE, zLabels GmbH, and IKEA Deutschland GmbH & Co KG."""
    # job_description = """'job_title': 'Junior Project Manager (gn) Programmkonzeption & Projektmanagement PR-Events', 'company_name': 'Quadriga Media Berlin GmbH', 'company_location': 'Berlin', 'company_info': 'Quadriga ist ein führendes Medien- und Weiterbildungsunternehmen im Herzen Berlins. Wir haben es uns zur Aufgabe gemacht, Professionals weiterzubilden, zu informieren und zu vernetzen. Daran arbeiten wir jeden Tag mit Freude und großer Leidenschaft – ob es um das Veranstalten von Tagungen, Seminare, E-Learnings, Kongressen und Awards geht, das Verlegen von Fachmedien oder die Betreuung von Verbänden. Vor Ort, digital oder hybrid bieten wir unseren Teilnehmer:innen dabei mit kreativen Formaten hochwertige und besondere Weiterbildungserlebnisse.', 'recruiter': 'Cara Perschke', 'recruiter_mail': 'recruiting@quadriga.eu', 'job_description': 'Intro #keepquestioning  Du hast Lust, Programme für Konferenzen zu entwickeln, tief in Trends und Entwicklungen im Bereich Kommunikationsmanagement einzutauchen und PR-Professionals in ihrer persönlichen und beruflichen Weiterentwicklung zu unterstützen?   Du bist kommunikationsstark, kreativ und strukturiert? Dann freuen wir uns auf deine Bewerbung. Als  Junior Project Manager (gn) Programmkonzeption & Projektmanagement PR-Events  bist du verantwortlich dafür, Konferenzen und Kongresse für PR-Professionals zu konzipieren, durchzuführen und weiterzuentwickeln (Konferenz Interne Kommunikation, Konferenz CEO-Kommunikation, Corporate Influencer Day, etc.). In der Position braucht es von dir Interesse für unsere Zielgruppe von PR-Professionals sowie deren Themen und Herausforderungen. Außerdem verfolgst du gerne technologische, ökonomische und gesellschaftspolitische Entwicklungen und kannst deren Bedeutung für verschiedene Branchen abschätzen.   Du hast ein gutes Gespür für Menschen und Themen? Dann bist du genau richtig bei uns im Team. Aufgaben Deine Verantwortung Konzeption und Erstellung hochwertiger Konferenzen und Kongresse (Themenentwicklung, Programmkonzeption, Formatentwicklung wie bspw. Unconferences, kreative Workshop-Formate, etc.)  Verantwortung für das Projektmanagement (Budget, Timings, Schnittstelle zu Marketing, Operations, Event, Einkauf)  Recherche zu relevanten Themen sowie Akquise von passenden Referent*innen inklusive detaillierte Absprache mit Referent*innen bezüglich Inhalt, Aufbau, Didaktik usw.  Qualitätsmanagement und Weiterentwicklung von digitalen und analogen Veranstaltungen  Zuarbeit bei der Erstellung von Marketingmaterial (Broschüre, Website, Newsletter, Anzeigen, Mailings)  Budget- und Umsatzkontrolle der Veranstaltungen im engen Austausch mit Teamlead  Stakeholder Management (Intern und extern, beispielsweise Referent*innen, Partner*innen, Berufsverbände) Anforderungen Deine Skills Abgeschlossenes Studium (bspw. im Bereich Sozialwissenschaften, Medienwissenschaften, Kommunikationswissenschaften, Pädagogik / Erwachsenenbildung oder Wirtschaftswissenschaften)  Mind. ein Jahr Berufserfahrung  Interesse für und bestenfalls Erfahrung mit unserer Zielgruppe von PR-Professionals, deren Themen und Herausforderungen (Interne Kommunikation, CEO-Kommunikation, Social Media Kommunikation, etc.) Wünschenswert: Erfahrung in Projektmanagement  Eigenverantwortliches Arbeiten mit einem hohen Maß an Kooperations- und Teamfähigkeit  Kommunikativ und schreibstark mit Freude am Verfassen von Texten  Strukturierte Arbeitsweise und Problemlösekompetenz  Deutsch auf Muttersprachniveau und gute Englischkenntnisse in Wort und Schrift Benefits Unsere Benefits Professionelle Weiterentwicklung steht bei uns im Fokus – mit individuell gestalteten Weiterbildungstagen sowie alltäglichem Zugang zu unseren relevanten Netzwerken, Publikationen, Events und Weiterbildungsprodukten. Werde Teil eines lebendigen Teams von 150 Mitarbeiter*innen, die gemeinsam intensiv arbeiten, diskutieren und feiern. Quadriga erlebst du Start Up-Kultur in einem etablierten, renommierten Unternehmen – mit viel Raum für neue Ideen, kurzen Entscheidungswegen, Transparenz und „Duz-Kultur“. Eine gute Work-Life-Balance ist uns wichtig. Wir bieten flexible, familienfreundliche Arbeitszeiten, individuelle Lösungen bezüglich des Arbeitsortes (Büro und/oder Mobile Office) und ein abwechslungsreiches Sportprogramm (u.a. in Kooperation mit Urban Sports) sowie eine betriebliche Altersvorsorge an. Arbeite im Herzen von Berlin, mit hervorragender Anbindung an den ÖPNV und grünem Innenhof.'"""
    # generator = CoverLetterGenerator(OPENAI_API_KEY, job_description, cv_text, "full", 0, "")
    # # job_extract = generator.relevant_job_info()
    # # print(job_extract)

    # cover_letter = generator.generate_application_letter()
    # print(cover_letter)