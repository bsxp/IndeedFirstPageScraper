import requests
from bs4 import BeautifulSoup

class JobPosting:

    def __init__(self, company, summary, salary, date, location, site):
        self.company = company
        self.summary = summary
        self.salary = salary
        self.date = date
        self.location = location
        self.site = site

class PostingFinder:

    allPostings = []

    cachedSearches={}

    def searchIndeed(self, jobTitle, location, doPrint=False):

        URL = f'https://www.indeed.com/jobs?q={jobTitle.replace(" ", "+")}&l={location.replace(" ", "%20")}'

        if URL in self.cachedSearches:
            return False

        responses = []

        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='resultsBodyContent')

        job_elems = results.find_all('div', class_='jobsearch-SerpJobCard unifiedRow row result')

        for job_elem in job_elems:

            company_elem = job_elem.find('span', class_='company')
            summary_elem = job_elem.find('div', class_='summary')
            salary_elem = job_elem.find('span', class_='salaryText')
            date_elem = job_elem.find('span', class_='date')
            location_elem = job_elem.find('div', class_='location')

            posting = JobPosting(company_elem, summary_elem, salary_elem, date_elem, location_elem, "Indeed")
            self.allPostings.append(posting)

            if doPrint is True:
                print('##########################')
                print("Company: " + company_elem.text, '\n')
                print("Summary: " + summary_elem.text, '\n')
                print("Salary not found" if type(salary_elem) is type(None) else salary_elem.text, '\n')
                print("Date: " + date_elem.text, '\n')
                print("Location not found" if type(location_elem) is type(None) else location_elem.text, '\n')
                print('##########################')


postings = PostingFinder()

postings.searchIndeed("software engineer", "Seattle WA", True)

