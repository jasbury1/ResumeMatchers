import os
import shutil
from resumeParse import get_skills_from_resume
from graphCreatition import read_graph
from jobParse import format_job_strings
from jobPredictor import rank_jobs
from flask import Flask, flash, request, redirect, render_template, url_for, session

app = Flask(__name__)
app.secret_key = "cant guess this"

KG_FILEPATH = "../knowledgegraph.edgelist"

# create new empty file path
print("creating new path")
UPLOAD_PATH = "../uploaded_files/"
if os.path.exists(UPLOAD_PATH):
    shutil.rmtree(UPLOAD_PATH)
os.makedirs(UPLOAD_PATH)
app.config['UPLOAD_PATH'] = UPLOAD_PATH


@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    # render index template
    return render_template("index.html", files=files)


@app.route('/', methods=["POST"])
def uploadFile():
    if request.form["submit_button"] == "Upload":
        # if no file uploaded, redirect to index.
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        # save file to uploads directory
        if file and file.filename != "":
            file.save(UPLOAD_PATH + file.filename)
    else:
        file = request.form["submit_button"]
        return redirect(url_for('getSkills', filename=file))

    # render index template
    return redirect(request.url)


@app.route('/parse/<filename>')
def getSkills(filename):
    skills = get_skills_from_resume(UPLOAD_PATH + filename)
    session[
        'skills'] = skills  # using a session variable to pass values between views
    return render_template("skills.html", skills=skills)


@app.route('/parse/<filename>', methods=["POST"])
def findJobs(filename):
    if request.form["submit_button"] == "Return":
        print("return")
        return redirect(url_for('index'))
    elif request.form["submit_button"] == "Find Job Postings":
        print("finding job postings")
        return redirect(url_for('getJobs', filename=filename))
    else:
        return redirect(request.url)


@app.route('/parse/<filename>/jobs')
def getJobs(filename):

    skills = session.get('skills', None)

    kg = read_graph(KG_FILEPATH)
    jobs = rank_jobs(kg, skills)
    jobs = format_job_strings(jobs)

    return render_template("jobs.html", jobs=jobs[:100])


@app.route('/parse/<filename>/jobs', methods=["POST"])
def navgiateJobs(filename):

    if request.form["submit_button"] == "Return":
        print("return")
        return redirect(url_for('index'))
    else:
        return redirect(request.url)


if __name__ == "__main__":
    app.run(debug=True)