import http.client
import json
import os

import requests
from flask import Flask, abort, jsonify, redirect, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from auth import AuthError, requires_auth
from models import Drink, Role, db_drop_and_create_all, setup_db

app = Flask(__name__)


@app.route("/")
def home_view():
    return "<h1>Welcome to Coffee Shop App!</h1>"


'''
To redirect the user for auth0 link
'''


@app.route("/authorize")
def authorize_user():
    url = "https://asraraljuhani.us.auth0.com/authorize?audience=" + \
        os.environ["audience"]
    url += "&response_type=token&client_id=" + \
        os.environ["client_id"]+"&client_secret="+os.environ["client_secret"]
    url += "&redirect_uri=https://asraraljuhani.us.auth0.com/oauth/token"
    return redirect(url)


setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
    GET /drinks
        it should require the 'get:drinks' permission
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where
    drinks is the list of drinks or appropriate status code indicating reason
    for failure
'''


@app.route('/drinks')
@requires_auth('get:drinks')
def drinks(payload):
    try:
        drinks = Drink.query.order_by(Drink.id).all()
        if drinks is None:
            abort(404)
        drinks = [drink.short() for drink in drinks]
    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'drinks': drinks
    })


'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks or appropriate status code
    indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drinks_detail(payload):
    try:
        drinks = Drink.query.order_by(Drink.id).all()
        drinks = [drink.long() for drink in drinks]
    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'drinks': drinks
    })


'''
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the newly created drink
    or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    try:
        title_data = request.get_json()['title']
        recipe_data = str(request.get_json().get('recipe'))
        permissions_number = len(payload['permissions'])

        # check created_by using number of permissions
        role = Role.query.filter(
            Role.permissions_number == permissions_number).one_or_none()
        # format data
        recipe_data = recipe_data.replace("\'", "\"")

        drink = Drink(title=title_data, recipe=recipe_data,
                      created_by=role.name)
        drink.insert()
    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'drinks': drink.long()
    })


'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the updated drink
    or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(payload, drink_id):
    if drink_id is None:
        abort(404)
    drink_id = str(drink_id)
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)
    try:
        title_data = request.get_json()['title']
        if title_data is not None:
            drink.title = title_data

        recipe_data = str(request.get_json().get('recipe'))
        if recipe_data is not None:
            # format data
            recipe_data = recipe_data.replace("\'", "\"")
            drink.recipe = recipe_data

        drink.update()
    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'drinks': [drink.title]
    })


'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
    where id is the id of the deleted record
    or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drinks_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drinks_id):
    try:
        drink = Drink.query.get(drinks_id)
        drink.delete()

    except Exception:
        if drink is None:
            abort(404)
        else:
            abort(500)

    return jsonify({
        'success': True,
        'delete': drinks_id
    })

# Error Handling


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


# @app.errorhandler(401)
# def unauthorized(error):
#     return jsonify({
#         'success': False,
#         'error': 401,
#         "message": "unauthorized"
#     }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'error': 403,
        "message": "forbidden"
    }), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500


'''
error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        'error': error.status_code,
        'message': error.error['description']
    }), error.status_code


if __name__ == '__main__':
    app.run()
