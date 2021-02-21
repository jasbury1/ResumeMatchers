from pyresparser import ResumeParser

def main():
    skills = get_skills_from_resume('../resources/resume-sample1.pdf')
    print(skills)

def get_skills_from_resume(resume_path):
    data = ResumeParser(resume_path).get_extracted_data()
    skills = data['skills']
    return [s.lower() for s in skills]

if __name__ == '__main__':
    main()

