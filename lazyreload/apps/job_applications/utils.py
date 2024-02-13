from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class JobAd():
    def __init__(self, url):
        self.url = url

        self.job_site = {
            'indeed': {
                'job_title': 'h2',
                'job_description': 'div#jobDescriptionText',
                'job_location': 'div.jobsearch-JobInfoHeader-subtitle',
                'job_type': 'div.jobsearch-JobMetadataHeader-item',
                'recruiter_name': 'div.jobsearch-InlineCompanyRating',
                'contact_email': 'div.jobsearch-InlineCompanyRating'
            },
            'linkedin': {
                'job_title': 'h1',
                'job_description': 'div#jobDescriptionText',
                'job_location': 'div.jobsearch-JobInfoHeader-subtitle',
                'job_type': 'div.jobsearch-JobMetadataHeader-item',
                'recruiter_name': 'div.jobsearch-InlineCompanyRating',
                'contact_email': 'div.jobsearch-InlineCompanyRating'
            },
            'glassdoor': {
                'job_title': 'h12',
                'job_description': 'div#jobDescriptionText',
                'job_location': 'div.jobsearch-JobInfoHeader-subtitle',
                'job_type': 'div.jobsearch-JobMetadataHeader-item',
                'recruiter_name': 'div.jobsearch-InlineCompanyRating',
                'contact_email': 'div.jobsearch-InlineCompanyRating'
            },
            'monster': {
                'job_title': 'h1',
                'job_description': 'div#jobDescriptionText',
                'job_location': 'div.jobsearch-JobInfoHeader-subtitle',
                'job_type': 'div.jobsearch-JobMetadataHeader-item',
                'recruiter_name': 'div.jobsearch-InlineCompanyRating',
                'contact_email': 'div.jobsearch-InlineCompanyRating'
            }
        }
        self.company_name = None
        self.job_title = None
        self.job_description = None
        self.job_location = None
        self.job_type = None
        self.recruiter_name = None
        self.contact_email = None

    def get_job_site(self):
        # Get the job site from the URL
        if 'indeed' in self.url:
            return self.job_site['indeed']
        elif 'linkedin' in self.url:
            return self.job_site['linkedin']
        elif 'glassdoor' in self.url:
            return self.job_site['glassdoor']
        elif 'monster' in self.url:
            return self.job_site['monster']
        else:
            return None
    
    def get_job_details(self):
        # Get the job details from the job ad URL
        response = requests.get(self.url).text
        soup = BeautifulSoup(response, 'html.parser')# parse the html content of the job ad
        self.job_title = soup.find("h2").text
        print(self.job_title)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.url)
        
        # decline cookies
        cookies = driver.find_element(By.XPATH, '//*[@id="onetrust-reject-all-handler"]')
        cookies.click()

        job_title = driver.find_element(By.XPATH, '//*[@id="jobsearch-ViewjobPaneWrapper"]/div/div/div/div[1]/div/div[2]/div[1]/h2/span')
        print(job_title.text)

if __name__ == "__main__":
    job_ad = JobAd('https://de.indeed.com/jobs?q=python&l=berlin&from=searchOnHP&vjk=dc7b92460b8aee87&advn=2386904480922046')
    job_ad.get_job_details()
    
