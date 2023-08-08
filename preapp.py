#!./.venv/bin/python
# -*- coding: utf-8 -*-

"""
    Flask Practice Exercises:
    - Extracting data of top rated movies from IMDb.
    - Saving it in a CSV file in following columns.
        1. Rank & Title
        2. Year
        3. IMDb Rating
    - Importing CSV file in SQLite table.

"""

# Standard library
from pathlib import Path
import sqlite3
import re

# Third-party library
from bs4 import BeautifulSoup
import pandas as pd
import requests


### Extracting data from IMDb using this URL https://www.imdb.com/chart/top/ 
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


### Import CSV file in SQLite table.:

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
