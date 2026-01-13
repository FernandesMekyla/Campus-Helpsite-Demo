from flask import Flask, render_template, request

app = Flask(

    __name__,
    template_folder='templates'

    )

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/times")
def times():
    return render_template("times.html")

@app.route("/thanks", methods =["POST"])
def thanks():
    name = request.form.get("name", "").strip()
    issue_type = request.form.get("issue_type", "").strip()
    return render_template("thanks.html", name=name, issue_type=issue_type)
