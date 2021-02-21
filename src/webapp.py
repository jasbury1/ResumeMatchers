import os
import shutil
from resumeParse import get_skills_from_resume
from flask import Flask, flash, request, redirect, render_template, url_for

app = Flask(__name__)

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
    return render_template("skills.html", skills=skills)

@app.route('/parse/<filename>', methods=["POST", "GET"])
def findJobs():
    if request.form["submit_button"] == "Return":
        print("return")
        return redirect(url_for('index'))
    else:
        return redirect(request.url(filename=filename))

if __name__ == "__main__":
    app.run(debug=True)