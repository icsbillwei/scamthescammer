from flask import Flask, jsonify
from .chatbot import chatbot_bp

app = Flask(__name__)

app.register_blueprint(chatbot_bp, url_prefix='/')

@app.route("/")
def home():
    return jsonify(message="Scam the Scammers service")


if __name__ == '__main__':
    app.run(debug=True)