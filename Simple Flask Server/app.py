from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Server says hello!!!'


@app.route('/hi-there')
def hi_there():
    return 'Server says hi there!!!'


@app.route('/bye')
def bye():
    return 'Server says bye!!!'


@app.route('/calc-sum', methods=['POST'])
def calc_sum():
    data = request.get_json()
    sum = data['a'] + data['b']
    result = {'result': sum}
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
