# What is Book Ace?
## ENGO 551 Winter 2021 Lab 1 Submission 
Book Ace is a Flask application allowing users to review and submit their book reviews through a catalogue of thousands of books. 

# Tech Stack
Flask, SQL, SCSS

# Notable Features
* User Authentication - Users can register for a new account, login and logout of the application
* Review Submission - Users can search for a book - provided it is saved in the catalogue, get access to the book's details (ISBN, Author, Published Year, etc.), and submit a numerical rating and a short review.
* API Requests - Users can submit a get request at ```/api/<ISBN>``` to receive detailed information on a book of their choice and reviews submitted on this application.

# File Structure
* /static - Contains .csv of all stored books and stylesheets
* /templates - Documents rendered via Jinja syntax, i.e All HTML pages 
* .gitignore - Specifies files ignored by Git
* application.py - All backend logic running the application
* import.py - Script to add all entries in books.csv to database
* requirements.txt - Configuration file for pip
* settings.py - Retrieves database URL 
