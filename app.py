from flask import Flask, render_template, request, redirect, url_for

from detector.email_detector import analyze_email
from detector.url_detector import analyze_url

from simulator.sample_emails import SAMPLE_EMAILS

from database.database import (
    initialize_database,
    save_email,
    save_url,
    get_email_history,
    get_url_history,
    dashboard_stats,
    report_stats
)

app = Flask(__name__)

initialize_database()


# =====================================
# LOGIN
# =====================================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )

    return render_template("login.html")


# =====================================
# DASHBOARD
# =====================================

@app.route("/dashboard")
def dashboard():

    stats = dashboard_stats()

    return render_template(

        "dashboard.html",

        stats=stats

    )


# =====================================
# EMAIL DETECTOR
# =====================================

@app.route("/detector", methods=["GET", "POST"])
def detector():

    score = None

    reasons = []

    recommendations = []

    email = ""

    if request.method == "POST":

        email = request.form["email"]

        score, reasons, recommendations = analyze_email(email)

        save_email(

            email,

            score,

            reasons,

            recommendations

        )

    return render_template(

        "detector.html",

        score=score,

        reasons=reasons,

        recommendations=recommendations,

        email=email

    )


# =====================================
# URL ANALYZER
# =====================================

@app.route("/url", methods=["GET", "POST"])
def url():

    score = None

    reasons = []

    recommendations = []

    if request.method == "POST":

        website = request.form["url"]

        score, reasons, recommendations = analyze_url(website)

        save_url(

            website,

            score,

            reasons,

            recommendations

        )

    return render_template(

        "url.html",

        score=score,

        reasons=reasons,

        recommendations=recommendations

    )
# =====================================
# SIMULATOR
# =====================================

@app.route("/simulator")
def simulator():

    return render_template(

        "simulator.html",

        emails=SAMPLE_EMAILS

    )


# =====================================
# AWARENESS
# =====================================

@app.route("/awareness")
def awareness():

    return render_template(

        "awareness.html"

    )


# =====================================
# REPORT
# =====================================

@app.route("/report")
def report():

    stats = report_stats()

    return render_template(

        "report.html",

        stats=stats

    )


# =====================================
# EMAIL HISTORY
# =====================================

@app.route("/email-history")
def email_history():

    history = get_email_history()

    return render_template(

        "email_history.html",

        history=history

    )


# =====================================
# URL HISTORY
# =====================================

@app.route("/url-history")
def url_history():

    history = get_url_history()

    return render_template(

        "url_history.html",

        history=history

    )


# =====================================
# RUN APPLICATION
# =====================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
