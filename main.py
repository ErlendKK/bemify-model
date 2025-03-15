import flask
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return flask.jsonify({
        "message": "Hello World!",
        "status": "success"
    })

@app.route('/increment', methods=['POST'])
def increment():
    # Get the JSON data from the request
    data = flask.request.json
    
    # Check if number is provided
    if 'number' not in data:
        return flask.jsonify({
            "error": "Missing 'number' in request",
            "status": "error"
        }), 400
    
    # Try to convert to integer and increment
    try:
        number = int(data['number'])
        result = number + 1
        return flask.jsonify({
            "original": number,
            "incremented": result,
            "status": "success"
        })
    except ValueError:
        return flask.jsonify({
            "error": "Invalid number format",
            "status": "error"
        }), 400

if __name__ == '__main__':
    app.run()