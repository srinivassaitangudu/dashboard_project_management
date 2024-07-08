from flask import Flask
from app.endpoints.dashboard import main

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.register_blueprint(main, url_prefix="/dashboard")

    # with app.app_context():
       
    return app
