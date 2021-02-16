import os

from flask import Flask, session, render_template, request, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

app = Flask(__name__)
app.config.from_pyfile('settings.py')

# Check for environment variable
if not app.config.get("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(app.config.get("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Login/landing page
@app.route("/", methods = ["GET", "POST"])
def index():
    # Post-registration
    if request.method == "POST":
        try:
            # Create login in DB
            username = request.form.get("newUsername")
            password = request.form.get("newPassword")
            print(username)
            print(password)
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", 
            {"username": username, "password": password})
            db.commit()
            flash(f"Please login with your new credentials for {username}")
            return render_template("login.html")
        except:
            return "Registration Unsuccessful."
    else:
        return render_template("login.html")

# Main route
@app.route("/logged_in", methods = ["GET", "POST"])
def logged_in():
    if request.method == "GET":
        return "Please go back and login."
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        session["login"] = username
        return render_template("index.html", username = username, password = password)

# Register page 
@app.route("/register")
def register():
    return render_template("register.html")

# Post registration page
@app.route("/register_success")
def register_success():
    return render_template("register_success.html")