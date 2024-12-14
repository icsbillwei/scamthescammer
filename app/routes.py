from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return jsonify(message="Welcome to the Flask app!")

@bp.route('/api/data')
def get_data():
    data = {"key": "value"}
    return jsonify(data)


"""
GPT suggested:

from flask import Flask, request

app = Flask(__name__)

@app.route("/sms", methods=["POST"])
def sms_webhook():
    from_number = request.form.get("From")
    body = request.form.get("Body")
    print(f"Message received from {from_number}: {body}")
    return "Message received", 200

if __name__ == "__main__":
    app.run(debug=True)

"""