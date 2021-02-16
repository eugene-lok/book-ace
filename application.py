import os
import requests

from flask import Flask, session, render_template, request, flash, jsonify
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

# Register page 
@app.route("/register")
def register():
    return render_template("register.html")

# Main route
@app.route("/logged_in", methods = ["GET", "POST"])
def logged_in():
    if request.method == "GET":
        return "Please go back and login."
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        # Validate login
        if db.execute("SELECT username FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount == 1:
            session["login"] = username
            return render_template("index.html", username = username, password = password)
        else:
            return "Invalid login." 
        
# Search results
@app.route("/search", methods = ["POST"])
def search():
    searchType = request.form.get("searchType")
    searchQuery = request.form.get("findBook")
    print(f'searchType{searchType}')
    print(f'findBook{searchQuery}')
    if searchType == 'isbn':
        searchResults = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn", {"isbn": "%" + searchQuery + "%"}).fetchall()
    elif searchType == 'author':
        searchResults = db.execute("SELECT * FROM books WHERE author LIKE :author", {"author": "%" + searchQuery + "%"}).fetchall()
    elif searchType == 'title':
        searchResults = db.execute("SELECT * FROM books WHERE title LIKE :title", {"title": "%" + searchQuery + "%"}).fetchall()
    else:
        return "How did this even happen?"
    # Validate search result 
    if searchResults != "[]":
        #searchJSON = jsonify(searchResults)
        return render_template("search.html", searchQuery = searchQuery, searchResults = searchResults)
    else:
        return "Search failed."

# Get book details
@app.route("/details", methods = ["POST"])
def getDetails():
    isbn = request.form.get("bookID")
    session["isbn"] = isbn
    # API request
    res = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": "isbn:" + isbn})
    bookInfo = res.json()
    title = bookInfo['items'][0]['volumeInfo']['title']
    authors = bookInfo['items'][0]['volumeInfo']['authors']
    year = bookInfo['items'][0]['volumeInfo']['publishedDate'][0:4]
    googleCount = bookInfo['items'][0]['volumeInfo']['ratingsCount']
    googleRating = bookInfo['items'][0]['volumeInfo']['averageRating']
    return render_template("details.html", isbn = isbn, title = title, authors = authors, year = year, googleCount = googleCount, googleRating = googleRating)

# Submit review
@app.route("/thankyou", methods = ["POST"])
def submitReview():
    username = session["login"]
    isbn = session["isbn"]
    rating = request.form.get("rating")
    review = request.form.get("review")
    # Submit to DB
    isDuplicate = db.execute("SELECT * FROM reviews WHERE username = :username AND isbn = :isbn", {"username": username,"isbn": isbn}).rowcount
    print(f'Duplicate?{isDuplicate}')
    if isDuplicate:
        return "You've already reviewed this book!"
    else:
        db.execute("INSERT INTO reviews (username, isbn, rating, review) VALUES (:username, :isbn, :rating, :review)", {"username":username, "isbn":isbn, "rating":rating, "review":review})
        db.commit()
        return render_template("thankyou.html")

# API access