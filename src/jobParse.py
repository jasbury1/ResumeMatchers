import requests
import json
from bs4 import BeautifulSoup

# File constants
skills_file_path = "../resources/skills_list.txt"
out_json_name = "../resources/scraped_jobs.json"

URLS = ['https://www.indeed.com/jobs?q=software+engineer&l=California']
skills_list = set(line.strip().lower() for line in open(skills_file_path))


class Job:
    def __init__(self, title, company, location, short_description, long_description):
        self.title = title
        self.company = company
        self.location = location
        self.short_description = short_description
        self.long_description = long_description
        self.skills = []

def main():
    jobs_list = []

    for URL in URLS:
        create_jobs(process_url(URL), jobs_list)

    write_job_json(jobs_list, out_json_name)

'''
Process URL:
    processes a URL to scrape it for jobs.
    Returns the data found for the jobs located at the url as a list
'''
def process_url(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='resultsCol')
    job_data = results.find_all(class_='jobsearch-SerpJobCard')
    return job_data

'''
Create Jobs:
    iterates through job data scraped from a URL
    Creates job objects and places them into the job_list parameter
'''
def create_jobs(job_data, jobs_list):
    for job in job_data:
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

        # Extract skills from the job listing and add to the job's skill list
        words = [''.join(filter(str.isalnum, w)).lower() for w in new_job.long_description.split(' ')]
        for word in words:
            if word in skills_list:
                new_job.skills.append(word)

        jobs_list.append(new_job)

'''
Write Jobs Json:
    Iterates through a list of job objects
    Writes specific data out ot a json file
'''
def write_job_json(jobs_list, out_json_name):
    jobs_dict = {}
    for job in jobs_list:
        key = "{} at: {} in: {}".format(job.title, job.company, job.location)
        jobs_dict[key] = job.skills
    with open(out_json_name, "w") as out_json:
        json.dump(jobs_dict, out_json, indent=4)

if __name__ == '__main__':
    main()
