from flask import Blueprint,request,  jsonify
from app.crud.project import Project
from app.utils.common import generate_response
from app.utils.http_code import *
from flask_cors import cross_origin


main = Blueprint('main', __name__)

@main.route("/project/get_my projects", methods=["GET"])
@cross_origin()
def get_my_projects():
    employee_id = request.args.get('email')
    projects = Project().get_my_projects(email= employee_id)

    return projects


@main.route("/project/project_view",methods=['GET'])
@cross_origin()
def get_project():
    project_id = request.args.get("project_id")
    project_info_raw = Project().get_project_info(project_id=project_id)

    return project_info_raw