# Coffee Shop

Coffee Shop app is a backend flask application that allows users to get, add, edit, and delete drinks at Udacity cafe.

## Features

The application has CRUD functionality as shown below:

1. get drinks information.
2. add drinks information.
3. edit drinks information.
4. delete drinks information.

## User Types (Roles)

The application has two types of user(roles) who are:
1. Barista, is someone who serves and provides customers.
2. A manager, is someone who manages and runs the coffee shop.

## User Permissions

- The Barista can ```get:drinks``` and ```post:drinks``` only.
- The Manager has all permissions, which are ```delete:drinks```, ```get:drinks```, ```get:drinks-detail```, ```patch:drinks```, and ```post:drinks```.


## Built with

* Auth0.
* Python.
* Flask Framework.
* Postgres.


## Getting Started

## Key Dependencies

- [Python 3.7](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) is an interpreted high-level general-purpose programming language.

- [Virtual Enviornment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) is a tool that helps to keep dependencies required by different projects separate by creating isolated python virtual environments for them.

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- PIP Dependencies install dependencies using this command to install all of the required packages we selected within the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## API Documentation

The application has 5 endpoints which are:

```js
GET '/drinks'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
{
    "success": True,
   "drinks": drinks: {
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```

```js
GET '/drinks-detail'
- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}
```

```js
POST '/drinks'
- Fetches questions for a cateogry specified by id request argument
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```

```js
PATCH '/drinks/${id}'
- Fetches questions for a cateogry specified by id request argument
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```

```js
DELETE '/drinks/${id}'
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.
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

