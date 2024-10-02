from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

# create the flask instance
app = Flask(__name__)
api = Api(app)

# connect to the mongo database
client = MongoClient('mongodb://db:27017')
db = client.SimilarityDB
users = db['users']


# checks user exists or not
def check_user_exists(user_name):
    return users.count_documents({
        'username': user_name
    }) == 0


# resource class for user registration
class Register(Resource):
    def post(self):
        # access the posted data
        request_data = request.get_json()

        # get the username and password
        user_name = request_data['username']
        password = request_data['password']

        # check user already exist or not
        is_user_exists = check_user_exists(user_name)
        if not is_user_exists:
            result_json = {
                'status': 301,
                'message': 'Username already exists'
            }

            return jsonify(result_json)

        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # insert the data to db
        users.insert_one({
            'username': user_name,
            'password': hashed_password,
            'tokens': 6
        })

        result_json = {
            'status': 200,
            'message': 'You successfully signed up for the API'
        }

        return jsonify(result_json)


# add the resource to API
api.add_resource(Register, '/register')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
