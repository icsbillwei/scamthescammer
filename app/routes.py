from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return jsonify(message="Welcome to the Flask app!")

@bp.route('/api/data')
def get_data():
    data = {"key": "value"}
    return jsonify(data)

