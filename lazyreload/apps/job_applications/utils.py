from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

class JobAdImporter:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            }
        self.driver = None
        self.soup = None

    def selenium_decorator(func):
        """
        Decorator to manage a Chrome WebDriver for data scraping.

        Args:
            func: The function to be decorated.

        Returns:
            A wrapper function that handles WebDriver setup and teardown.
        """
        def wrapper(self, *args, **kwargs):
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("detach", True)
            self.driver = webdriver.Chrome(options=chrome_options)
            try:
                self.driver.get(self.url)
                time.sleep(2)
                result = func(self, *args, **kwargs) # call the decorated function
                return result
            except Exception as e:
                print(f"Error during information retrieval: {e}")
            # finally:
            #     self.driver.quit()
        return wrapper
    
    def soup_decorator(func):
        """
        Decorator to manage a BeautifulSoup object for data scraping.

        Args:
            func: The function to be decorated.

        Returns:
            A wrapper function that handles BeautifulSoup setup and teardown.
        """
        def wrapper(self, *args, **kwargs):
            website = requests.get(self.url, headers=self.headers)
            try:
                self.soup = BeautifulSoup(website.text, "html.parser")
                result = func(self, *args, **kwargs) # call the decorated function
                return result
            except Exception as e:
                print(f"Error during information retrieval: {e}")
        return wrapper


    @selenium_decorator
    def get_indeed_information(self):
        """
        Retrieves job ad information from Indeed with Selenium, returns a dictionary.
        """

        # decline cookies
        cookies = self.driver.find_element(By.XPATH, '//*[@id="onetrust-reject-all-handler"]')
        cookies.click()
        print("Cookies declined")
        # get job title
        time.sleep(3)
        try:
            job_title = self.driver.find_element(By.XPATH, '//*[@id="jobsearch-ViewjobPaneWrapper"]/div/div/div/div[1]/div/div[2]/div[1]/h2/span')
            company_name = self.driver.find_element(By.XPATH, '//*[@id="jobsearch-ViewjobPaneWrapper"]/div/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div[1]/span/a')
            company_location = self.driver.find_element(By.XPATH, '//*[@id="jobsearch-ViewjobPaneWrapper"]/div/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div')
            job_description = self.driver.find_element(By.XPATH, '//*[@id="jobDescriptionText"]')
        except NoSuchElementException:
            print("Element not found")

        return {
            "job_title": job_title.text.replace("- job post", "").strip(),
            "company_name": company_name.text.strip(),
            "company_location": company_location.text.strip(),
            "job_description": job_description.text.replace("\n"," ").strip()
            }
        
    @soup_decorator
    def get_baito_information(self):
        """
        Retrieves job ad information from Baito with BeautifulSoup, returns a dictionary.
        """
        job_title = self.soup.find("span", {"data-br": ":R2r3brrqnlenla:"})

        print(job_title.text.replace("Stellenausschreibung: ", "").strip())
# <span data-br=":R2r3brrqnlenla:" data-brr="1" style="display:inline-block;vertical-align:top;text-decoration:inherit;text-wrap:balance">Stellenausschreibung: Mitarbeiter*in Controlling - ATZE Musiktheater</span>


if __name__ == "__main__":
    #indeed_ad = JobAdImporter('https://de.indeed.com/jobs?q=python&l=berlin&from=searchOnHP&advn=95263882141188&vjk=2fcd8a5b9ce55739')
    #information = indeed_ad.get_indeed_information()
    #print(information)
    
    baito_ad = JobAdImporter('https://www.getbaito.com/de/job/stellenausschreibung-mitarbeiterin-controlling-atze-musiktheater-atze-musiktheater-gmbh?location=berlin#topOfDescription')
    baito_ad.get_baito_information()