import requests
import json
from bs4 import BeautifulSoup

# File constants
skills_file_path = "../resources/skills_list.txt"
out_json_name = "../resources/scraped_jobs.json"

URLS = [
    'https://www.indeed.com/jobs?q=Softwaer+Engineer&l=California&radius=100&limit=50&sort=date'
]

skills_list = set(line.strip().lower()
                  for line in open(skills_file_path, "r", encoding='utf-8'))


class Job:
    def __init__(self, title, company, location, short_description,
                 long_description):
        self.title = title
        self.company = company
        self.location = location
        self.short_description = short_description
        self.long_description = long_description
        self.skills = []


def main():
    jobs_list = []

    for i in range(50, 10001, 50):
        URLS.append(
            "https://www.indeed.com/jobs?q=Software+Engineer&l=California&radius=100&sort=date&limit=50&start={0}"
            .format(i))

    for URL in URLS:
        create_jobs(process_url(URL), jobs_list)

    write_job_json(jobs_list, out_json_name)


'''
Process URL:
    processes a URL to scrape it for jobs.
    Returns the data found for the jobs located at the url as a list
'''


def process_url(URL):
    try:
        page = requests.get(URL)
    except requests.exceptions.ConnectionError:
        print("site cannot be reached")
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='resultsCol')
    if results is not None:
        job_data = results.find_all(class_='jobsearch-SerpJobCard')
        return job_data
    return []


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
            try:
                job_page = requests.get(job_url)
            except requests.exceptions.ConnectionError:
                print("site cannot be reached")
            job_soup = BeautifulSoup(job_page.content, 'html.parser')
            job_description = job_soup.find(id='jobDescriptionText')

        job_description_parsed = None
        if job_description is not None:
            job_description_parsed = job_description.text.strip()

        # Create Job class and insert into Job array
        new_job = Job(title_info.text.strip(), company_info.text.strip(),
                      location_info.text.strip(),
                      description_info.text.strip(), job_description_parsed)

        # Extract skills from the job listing and add to the job's skill list

        if new_job.long_description is not None:
            words = [
                ''.join(filter(str.isalnum, w)).lower()
                for w in new_job.long_description.split(' ')
            ]
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
        key = "{}; {}; {}".format(job.title, job.company, job.location)
        jobs_dict[key] = job.skills
    with open(out_json_name, "w") as out_json:
        json.dump(jobs_dict, out_json, indent=4)


'''
Format Job Strings:
    Iterates through a list of job strings
    and format them into a more pleasantly
    readable format for the web page
'''


def format_job_strings(jobs):
    formatted_jobs = []
    for job in jobs:
        job = job.replace("_", " ")
        split = job.split('; ')
        if len(split) >= 3:
            title_with_addition = split[0].replace(" ", "+")
            company_with_addition = split[1].replace(" ", "+")
            location_with_addition = split[2].replace(" ", "+")
            location_with_addition = location_with_addition.replace(",", "%2C")
            split.append("https://www.indeed.com/jobs?q=" +
                         title_with_addition + "&l=" + location_with_addition +
                         "&rbc=" + company_with_addition)
            formatted_jobs.append(split)

    return formatted_jobs


#https://www.indeed.com/jobs?q=UI+AngularJS+Bootstrap+Developer&l=Austin%2C+TX

if __name__ == '__main__':
    main()
