import requests
from bs4 import BeautifulSoup

class Job:
    def __init__(self, title, company, location, short_description, long_description):
        self.title = title
        self.company = company
        self.location = location
        self.short_description = short_description
        self.long_description = long_description
        self.skills = []

skills_file_path = "../resources/skills_list.txt"
URL = 'https://www.indeed.com/jobs?q=software+engineer&l=California'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='resultsCol')
jobs = results.find_all(class_='jobsearch-SerpJobCard')

jobs_list = []
skills_list = set(line.strip() for line in open(skills_file_path)



for job in jobs:
    # Get generic job information
    title_info = job.find('h2', class_='title')
    company_info = job.find('span', class_='company')
    location_info = job.find('span', class_='location')
    description_info = job.find('div', class_='summary')
    job_url = "https://www.indeed.com" + title_info.a['href']
    if None in (title_info, company_info, location_info, description_info):
        continue

    # Get job description information
    if job_url is not None:
        job_page = requests.get(job_url)
        job_soup = BeautifulSoup(job_page.content, 'html.parser')
        job_description = job_soup.find(id='jobDescriptionText')

    job_description_parsed = None
    if job_description is not None:
        job_description_parsed = job_description.text.strip()

    # Create Job class and insert into Job array
    new_job = Job(title_info.text.strip(),
                  company_info.text.strip(),
                  location_info.text.strip(),
                  description_info.text.strip(),
                  job_description_parsed)

    jobs_list.append(new_job)

# Test that jobs_list is filled
for job in jobs_list:
    print(job.title)
    print(job.company)
    print(job.location)
    print(job.short_description)
    print(job.long_description)
