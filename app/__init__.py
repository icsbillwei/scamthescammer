from flask import Flask

def create_app():
    main = Flask(__name__)

    from .main import bp as main_bp
    main.register_blueprint(main_bp)

    return main