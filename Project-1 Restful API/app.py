from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

# Creating connection to mongo database
client = MongoClient("mongodb://db:27017")

# Accessing the db aNewDB
db = client.aNewDB

# Accessing the collection userNum from aNewDB
user_num = db['userNum']

# Insert column num_of_users to userNum
user_num.insert_one({
    'num_of_users': 0
})

# Creating a class to handle user visit requests

class Visit(Resource):
    def get(self):
        prev_num = user_num.find({})[0]['num_of_users']
        new_num = prev_num + 1
        user_num.update_one({}, {'$set': {'num_of_users': new_num}})
        return str('Hello user ') + str(new_num)



def validate_data(data, function_name):
    if function_name in ['addition', 'subtraction', 'multiplication']:
        if 'a' not in data and 'b' not in data:
            return 301
        else:
            return 200
    elif function_name == 'division':
        if 'a' not in data and 'b' not in data:
            return 301
        elif int(data.get('b')) == 0:
            return 302
        else:
            return 200


class Add(Resource):
    def post(self):
        # parse the request JSON body
        data = request.get_json()

        status_code = validate_data(data, 'addition')

        if status_code != 200:
            return {
                'message': 'Invalid number of data',
                'status_code': status_code
            }

        value = data.get('a', 0) + data.get('b', 0)
        result = {
            'value': value,
            'status_code': status_code
        }

        return jsonify(result)


class Subtract(Resource):
    def post(self):
        # parse the request JSON body
        data = request.get_json()

        status_code = validate_data(data, 'subtraction')

        if status_code != 200:
            return {
                'message': 'Invalid number of data',
                'status_code': status_code
            }

        value = data.get('a', 0) - data.get('b', 0)
        result = {
            'value': value,
            'status_code': status_code
        }

        return jsonify(result)


class Multiply(Resource):
    def post(self):
        # parse the request JSON body
        data = request.get_json()

        status_code = validate_data(data, 'multiplication')

        if status_code != 200:
            return {
                'message': 'Invalid number of data',
                'status_code': status_code
            }

        product = data.get('a', 0) * data.get('b', 0)
        result = {
            'value': product,
            'status_code': status_code
        }

        return jsonify(result)


class Divide(Resource):
    def post(self):
        # parse the request JSON body
        data = request.get_json()

        status_code = validate_data(data, 'division')

        if status_code != 200:
            return {
                'message': 'An error occurred',
                'status_code': status_code
            }

        value = int(data.get('a', 0)) * 1.0 / int(data.get('b', 0))
        result = {
            'value': value,
            'status_code': status_code
        }

        return jsonify(result)


# Add resource to the API
api.add_resource(Add, '/addition')
api.add_resource(Subtract, '/subtraction')
api.add_resource(Multiply, '/multiplication')
api.add_resource(Divide, '/division')
api.add_resource(Visit, '/visit')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
