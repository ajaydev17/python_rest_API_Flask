from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


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

if __name__ == '__main__':
    app.run(debug=True)
