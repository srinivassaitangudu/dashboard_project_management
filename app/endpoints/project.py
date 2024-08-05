from flask import Blueprint,request,  jsonify
from app.crud.project import Project
from app.utils.common import generate_response
from app.utils.http_code import *
from flask_cors import cross_origin
# from app.endpoints.api import main


project = Blueprint('project', __name__)

@project.route("/get_all_projects", methods=["GET"])
@cross_origin()
def get_all_projects():
    projects = Project().get_all_projects()

    return projects


@project.route("/project_view",methods=['GET'])
@cross_origin()
def get_project():
    try:
        project_id = request.args.get("project_id")
        project_info = Project().get_project_info(projectid=project_id)

        return generate_response(data=project_info, status=200)
    except Exception as e:
        return generate_response(message="Some error occured while fetching project info!", status=400 )


@project.route("/get_create_task_info", methods=["GET"])
@cross_origin()
def get_create_task_info():
    project_id = request.args.get("project_id")

    try:
        return jsonify(Project().get_create_task_info(project_id=project_id))
    except Exception as e:
        return generate_response(status=400, message= e)
 


@project.route("/create_task", methods=["POST"])
@cross_origin()
def create_task():
    data = request.get_json()
    is_new = data.get("is_new")
    
    if is_new:
        data["taskid"] = Project().create_new_task(data.get("taskname"))[0]
    
    projecttaskid = Project().add_new_task_to_project(task_id =data["taskid"], project_id=data["projectid"], function_id=data["functionid"],assigneeemail= data["assigneeemail"],exception= data["exception"], special_instruction=data["special_instruction"], weightage= data["weightage"],duedate= data["duedate"], createdby= data["createdby"] )

    return jsonify(projecttaskid)

@project.route("/delete_task_in_project", methods=["POST"]) 
@cross_origin()
def delete_task_in_project():
    data = request.get_json()

    projecttaskid = data.get("projectaskid")
    try:
        Project().delete_task_in_project( project_task_id=projecttaskid)
        return jsonify({"message":"Task Deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message":"Task deletion failed!", "data":e}), 400
    
