import requests
from bs4 import BeautifulSoup

URL = 'https://www.indeed.com/jobs?q=software+engineer&l=California'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='resultsCol')
jobs = results.find_all(class_='jobsearch-SerpJobCard')

for job in jobs:
    title_info = job.find('h2', class_='title')
    company_info = job.find('span', class_='company')
    location_info = job.find('span', class_='location')
    description_info = job.find('div', class_='summary')
    if None in (title_info, company_info, location_info, description_info):
        continue
    print(title_info.text.strip())
    print(company_info.text.strip())
    print(location_info.text.strip())
    print(description_info.text.strip())
    print()