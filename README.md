# Gad-repo
#### Gaditek Project

---

## login form app using Python Flask Framework
**I have used Beautiful Soup, Selenium, Excel, VS Code and other tools.**


Extract data of top rated movies from IMDb using this URL _https://www.imdb.com/chart/top/_ and save it in a CSV file in following columns.
_1. Rank & Title_
_2. Year_
_3. IMDb Rating_

Example data:

| Rank & Title              | Year   | IMDb Rating  |
| :---                      | :----: |   ---:       |
| The Shawshank Redemption  |  1994  |   9.2        |
| The Godfather             |  1972  |   9.1        |
| The Godfather: Part II    |  1974  |   9.0        |


Create a Flask web with following routes.
> 1. /
> 2. /login
> 3. /signup
> 4. /movies

>> / would accept only GET request method and would display two options:
>> 1. Login
>> 2. Sign up

login would accept both GET and POST request methods. GET request display login page with login form which has two options username and password while POST request will be used to perform login itself. In case of unsuccessful login, user should return to login page.

/signup would accept both GET and POST request methods. GET request display sign up page with sign up form which should have five options email , firstname , lastname , username and password while POST request will be used to perform sign up itself and store user data in SQLite database.

In case of successful login, movies list should be show to the user in form of HTML table with following columns.
> 1. Rank & Title
> 2. Year
> 3. IMDb Rating

> Note:
> - You may add use any CSS framework for the aesthetic purpose.
> - Use a base template for HTML pages and extend that template where possible.
> - Use Jinja template where required or give ease of use.
> - Error page(s) could be use to give a better flow to the web application.


***


