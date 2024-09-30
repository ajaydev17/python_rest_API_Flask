from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db = client.SentencesDatabase
users = db['users']


def verify_username_password(user_name, password):
    # get the hashed password
    hashed_password = users.find({
        'username': user_name
    })[0]['password']

    return bcrypt.hashpw(password.encode('utf8'), hashed_password) == hashed_password


def count_tokens(user_name):
    tokens = users.find({
        'username': user_name
    })[0]['tokens']

    return tokens


class Register(Resource):
    def post(self):
        # get the data from post request
        request_data = request.get_json()

        # extracting username and password data
        user_name = request_data['username']
        password = request_data['password']

        # hashing the password before saving to db
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # storing the username and password into SentencesDatabase
        users.insert_one({
            'username': user_name,
            'password': hashed_password,
            'sentence': '',
            'tokens': 6
        })

        result_json = {
            'status': 200,
            'message': 'You have successfully signed up for the API.'
        }

        return jsonify(result_json)


class Store(Resource):
    def post(self):

        # get the request data
        request_data = request.get_json()

        # access the data
        user_name = request_data['username']
        password = request_data['password']
        sentence = request_data['sentence']

        # verify the username and password match
        is_verified = verify_username_password(user_name, password)

        if not is_verified:
            result_json = {
                'status': 302,
                'message': 'Invalid username or password'
            }

            return jsonify(result_json)

        # verify if the user has enough tokens
        number_of_tokens = count_tokens(user_name)

        if number_of_tokens <= 0:
            result_json = {
                'status': 301,
                'message': 'User has not enough tokens.'
            }

            return jsonify(result_json)

        # update the sentence and token
        users.update_one({
            'username': user_name
        }, {
            '$set': {
                'sentence': sentence,
                'tokens': number_of_tokens - 1
            }
        })

        result_json = {
            'status': 200,
            'message': 'Sentence saved successfully'
        }

        return jsonify(result_json)


class Get(Resource):
    def post(self):

        # get the request data
        request_data = request.get_json()

        # access the data
        user_name = request_data['username']
        password = request_data['password']

        # verify the username and password match
        is_verified = verify_username_password(user_name, password)

        if not is_verified:
            result_json = {
                'status': 302,
                'message': 'Invalid username or password'
            }

            return jsonify(result_json)

        # verify if the user has enough tokens
        number_of_tokens = count_tokens(user_name)

        if number_of_tokens <= 0:
            result_json = {
                'status': 301,
                'message': 'User has not enough tokens.'
            }

            return jsonify(result_json)

        # get the sentence value
        sentence = users.find({
            'username': user_name
        })[0]['sentence']

        # update the token
        users.update_one({
            'username': user_name
        }, {
            '$set': {
                'tokens': number_of_tokens - 1
            }
        })

        result_json = {
            'status': 200,
            'sentence': sentence
        }

        return jsonify(result_json)


# add the resources to api
api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
