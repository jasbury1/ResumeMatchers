import os
from resumeParse import get_skills_from_resume
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/', methods = ["POST", "GET"])
def uploadFile():
    if request.method == "POST":
        if "file" not in request.files:
            #flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            #flash("No selected file")
            return redirect(request.url)
        if file:
            skills = get_skills_from_resume(file)
            return {"skills" : skills}
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)