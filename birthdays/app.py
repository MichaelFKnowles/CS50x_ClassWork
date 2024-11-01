import os
from datetime import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if not request.form.get("name") or not request.form.get("birthday"):
            return render_template("failure.html")
        name = request.form.get("name")
        date = datetime.strptime(request.form.get("birthday"), "%Y-%m-%d").date()
        m = date.month
        d = date.day
        # TODO: Add the user's entry into the database
        db.execute("INSERT INTO birthdays (name, day, month) VALUES(?, ?, ?)", name, d, m)
        return redirect("/")

    else:
        # birthdays()
        # TODO: Display the entries in the database on index.html
        return render_template("birthdays.html")


@app.route("/birthdays", methods=["GET"])
def birthdays():
    birthdays = db.execute("SELECT * FROM birthdays LIMIT 50")
    # birthdays = jsonify(birthdays)
    # return birthdays
    # return render_template("birthdays.html", birthdays=birthdays)
    return jsonify(birthdays)
