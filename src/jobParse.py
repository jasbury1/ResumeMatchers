import requests
from bs4 import BeautifulSoup

URL = 'https://www.monster.com/jobs/search/?q=Software-Developer&where=California'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='ResultsContainer')
jobs = results.find_all('section', class_='card-content')

for job in jobs:
    title_info = job.find('h2', class_='title')
    company_info = job.find('div', class_='company')
    location_info = job.find('div', class_='location')
    if None in (title_info, company_info, location_info):
        continue
    print(title_info.text.strip())
    print(company_info.text.strip())
    print(location_info.text.strip())
    print()