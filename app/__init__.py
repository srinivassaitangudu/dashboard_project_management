from flask import Flask
from app.endpoints.dashboard import home
from app.endpoints.project import project

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.register_blueprint(home, url_prefix="/dashboard")
    app.register_blueprint(project, url_prefix="/project")
       
    return app
