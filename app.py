#!./.venv/bin/python
# -*- coding: utf-8 -*-

"""
    Flask Practice Exercise:
    - Extracting data of top rated movies from IMDb.
    - Saving it in a CSV file.
    - Importing CSV file in SQLite table.
    - Login Form
    - Sign up Form
    - In case of successful login, movies list would be displayed.
"""

# Standard library
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from pathlib import Path
import sqlite3
import re

# Third-party library
from bs4 import BeautifulSoup
import pandas as pd
import requests


### Extract data of top rated movies from IMDb using this URL https://www.imdb.com/chart/top

url = 'http://www.imdb.com/chart/top'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

movies = soup.select('td.titleColumn')
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]

imdb = []

# Store data 
for index in range(0, len(movies)):
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index))+1:-7]
    year = re.search('\((.*?)\)', movie_string).group(1)
    data = {"movie_title": movie_title,
            "year": year,
            "rating": ratings[index],}
    imdb.append(data)

# Create dataframe 
dataframe_columns = ['movie_title', 'year', 'rating']
dataframe = pd.DataFrame(columns=dataframe_columns)

# Save in CSV file
for i in range(0, len(imdb)):
    dataframe.at[i,'movie_title'] = imdb[i]['movie_title']
    dataframe.at[i,'year'] = imdb[i]['year']
    dataframe.at[i,'rating'] = imdb[i]['rating']
dataframe.to_csv('imdb_data.csv')


### Import CSV file in SQLite table.

# Create database file 
Path('imdb_data.db').touch()
conn = sqlite3.connect('imdb_data.db')
c = conn.cursor()

# Store data from csv file into database
df = pd.read_csv('imdb_data.csv', index_col=0)
df.to_sql('tmovies', conn, if_exists='append', index=False)

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS users (username text, password text, email varchar, firstname text, lastname text)''')
c.execute('''CREATE TABLE IF NOT EXISTS tmovies (movie_title text, year int, rating float)''')
 

# Create instance of Flask
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


""" / would accept only GET request method and would display two options Login & Sign up """
# Route to Home
@app.route("/")
def home():
    return render_template("home.html")


""" 
    /login would accept both GET and POST request methods. GET request display login page with login form which has two options username 
    and password while POST request will be used to perform login itself. In case of unsuccessful login, user should return to login page
"""
# Route to Login User
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get login details from user
        username = request.form.get("username")
        password = request.form.get("password")
        if not (username and password):
            return render_template("error.html", message= 'username or password missing')
        # then redirect user to movie list
        with sqlite3.connect('imdb_data.db') as conn:
            c = conn.cursor()           
            username = c.execute("SELECT username from users WHERE username= ? AND password = ?", (username, password)).fetchone()
            conn.commit()
            if not username: 
                return render_template('error.html',  message='login failed')
            else:
                return redirect("/movies") 
    return render_template("login.html")


""" /signup would accept both GET and POST request methods. GET request display sign up page with sign up form which should have five 
    options email , firstname , lastname , username and password while POST request will be used to perform sign up itself and store 
    user data in SQLite database.
"""
# Route to SignUp user
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Get login details from user
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        if not (username and password and email and firstname and lastname):
            return render_template("error.html", message= 'Fill all the fields')
        # Redirect to login page
        with sqlite3.connect('imdb_data.db') as conn:
            c = conn.cursor()  
            # Check if username already exists 
            # name = 
            c.execute("SELECT username FROM users").fetchall()
            conn.commit()
            conn.close()
            print(c)
            # if username not in name:
            #     c.execute("INSERT INTO users (username,password, email, firstname, lastname) VALUES (?,?,?,?,?)", (username, password, email, firstname, lastname))
            #     conn.commit()
            #     print("username true")
            #     return redirect("/movies")
            # else:
            #     return render_template('error.html',  message='Username already exists.')
    return render_template("signup.html")


""" In case of successful login, movies list should be show to the user in form of HTML table with columns; 
    Rank & Title, Year, IMDb Rating
"""
# Route to Movies Page      
@app.route("/movies", methods=["GET", "POST"])
def movies():
    # if request.method == "POST":
    session["name"] = request.form.get("name")
    with sqlite3.connect('imdb_data.db') as conn:
        c = conn.cursor()
        movies = c.execute('''SELECT * FROM tmovies''').fetchall()
        conn.commit()
        return render_template("movies.html", movies=movies)
    return render_template('error.html',  message='login failed')   


@app.route('/logout')
def logout():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
