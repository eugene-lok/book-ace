import csv
import os

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

# Set up database
engine = create_engine("DATABASE_URL")
db = scoped_session(sessionmaker(bind=engine))

def main():
    try:
        db.execute("CREATE TABLE books (isbn varchar, title varchar, author varchar, year integer)")
        db.commit()

        allBooks = csv.reader(open("static/books.csv"))
        # store books in database 
        for isbn, title, author, year in allBooks:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn": isbn, "title": title, "author": author, "year": year})
        db.commit()
    except:
        print("Error")   

if __name__ == "__main__":
    main()
