# Coffee Shop

Coffee Shop app is a backend flask application that allows users to get, add, edit, and delete drinks at Udacity cafe.

## Features

The application has CRUD functionality as shown below:

1. get drinks information.
2. add drinks information.
3. edit drinks information.
4. delete drinks information.

## Built with

* Auth0.
* Python.
* Flask Framework.
* Postgres.

## Deploy to Heroku

[Heroku URL](https://coffee-shop-asrar.herokuapp.com/)


## User Types (Roles)

The application has two types of user(roles) who are:
1. Barista, is someone who serves and provides customers.
2. A manager, is someone who manages and runs the coffee shop.

## User Permissions

| Role Name     | permissions|
| ------------- |:-------------:|
| Barista       | ```get:drinks``` and ```post:drinks``` only |
| Manager       | ```delete:drinks```, ```get:drinks```, ```get:drinks-detail```, ```patch:drinks```, and ```post:drinks```      |

## Instructions To Setup Authentications
We have two steps to setup the authentication:

1. Enter the [application authorized endpoint](https://coffee-shop-asrar.herokuapp.com/authorize) using this login info:

| Email                               | Password             | Role    |
| ----------------------------------- |:--------------------:| -------:|
| coffeeshop.asrar.manager@gmail.com  | ******************** | Manager |
| coffeeshop.asrar.barista@gmail.com  | ******************** | Barista |

2. After login takes the access_token from the URL and saves it to use with the proper endpoint as shown in **User Permissions** above.

Finally, You can use **Postman** with JWT token to run and test the endpoints.

> Note: You can verify the generated token using [jwt.io](https://jwt.io/) website. 

## Getting Started

### Key Dependencies

- [Python 3.7](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) is an interpreted high-level general-purpose programming language.

- [Virtual Enviornment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) is a tool that helps to keep dependencies required by different projects separate by creating isolated python virtual environments for them.

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

### Install dependencies

install dependencies using this command to install all of the required packages we selected within the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
### Database Setup

You have two options,

First you can use an external database and add their URL using this command below in the terminal. 

```bash
export SQL_DATABASE_URI=Your_DataBase_URL
```
or create it locally and add their URL using the same command above.

### Config Auth Variables 

Using these commands in the terminal, you can config Auth Variables on the project:
```bash
export audience=Your_audience;
export client_id=Your_client_id;
export client_secret=Your_client_secret;
```

### Running the server

from the root directory, run:

```bash
export FLASK_APP=app
flask run --reload
```

The ```--reload``` flag will detect file changes and restart the server automatically.

The server will run on http://localhost:5000.

## API Documentation

The application has 5 endpoints which are:

```js
GET '/drinks'
- Fetches drinks info.
- Request Arguments: None
- Returns: An object with an array of drinks contains their ids, titles, and created info.
{
    'drinks': [
        {
            'created_by': Manager,
            'id': 1,
            'title': 'water'
        },
    ],
    'success': true
}
```

```js
GET '/drinks-detail'
- Fetches drinks info in details.
- Request Arguments: None
- Returns: An object with an array of drinks info contains their full info from their ids, titles, recipe, and created info.
{
    'drinks': [
        {
            'created_by': 'Manager',
            'id': 1,
            'recipe': [
            {
               'color': 'blue',
               'name': 'water',
               'parts': 1
            }
            ],
            'title': 'water'
        }
    ],
    'success': true
}
```

```js
POST '/drinks'
- Fetches adding drink info
- Request Arguments: None
- Returns: An object with an array of drinks info contains their full info from their ids, titles, recipe, and created info.
{
    'drinks': [
        {
            'created_by': 'Manager',
            'id': 2,
            'recipe': [
            {
               'color': 'white',
               'name': 'milk',
               'parts': 1
            },
            {
               'color': 'green',
               'name': 'matcha',
               'parts': 1
            },
            ],
            'title': 'matcha latte'
        }
    ],
    'success': true
}
```

```js
PATCH '/drinks/${id}'
- Fetches drink info by id request argument
- Request Arguments: id - integer
- Returns: the updated drink name and the appropriate HTTP status code description.
{
    'drinks': 'Tea',
    'success': true
}
```

```js
DELETE '/drinks/${id}'
- Deletes a specified drink using its id
- Request Arguments: id - integer
- Returns: the appropriate HTTP status code description and the id of the deleted drink.
{
    'delete': 1,
    'success': true
}

```

## Errors

The Trivia app API uses the following error codes:

| Error Code |        Meaning        |
| ---------- | :-------------------: |
| 400        |      bad request      |
| 403        |      forbidden        |
| 404        |  resource not found   |
| 405        |  method not allowed   |
| 422        |     unprocessable     |
| 500        | internal server error |

#### Errors are returned in the following JSON format:

```js
{
'success': False,
'error': 400,
'message': 'bad request'
}
```

## Testing

To run the tests, run

```js
python test_flaskr.py
```
