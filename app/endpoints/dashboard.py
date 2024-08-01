from flask import Blueprint,request,  jsonify
from app.crud.dashboard import Dashboard
from app.utils.common import generate_response
from app.utils.http_code import *
from flask_cors import cross_origin
# from app.endpoints.api import main


home = Blueprint('home', __name__)

@home.route("/health", methods=['GET'])
@cross_origin()
def health_check():
    return jsonify({"status": "UP"}), 200

@home.route("/open_tasks", methods=["GET"])
@cross_origin()
def get_open_tasks():
    email = request.args.get('email')

    open_tasks = Dashboard().get_open_tasks(employee_id=email)
    return jsonify({'open_tasks':open_tasks})

@home.route("/closed_tasks", methods=["GET"])
@cross_origin()
def get_closed_tasks():
    email = request.args.get('email')

    closed_tasks = Dashboard().get_closed_tasks(employee_id=email)
    return jsonify({"closed_tasks":closed_tasks})


@home.route("/change_task_status", methods=["POST"])
@cross_origin()
def change_task_status():
    input_data =request.get_json()

    try:
        Dashboard().change_status(employee_id=input_data["email"], project_task_id=input_data["project_task_id"], status=input_data["status"], updated_by=input_data.get("updated_by", None))
        return generate_response(message="Status updated!", status= HTTP_200_OK)
    except Exception as e:
        return generate_response(message=e, status=HTTP_400_BAD_REQUEST)
# @home.route("/change_task_status", methods=["POST"])
# @cross_origin()
# def change_task_status():
#     input_data = request.get_json()

#     try:
#         Dashboard().change_status(employee_id=input_data["email"], project_task_ids=input_data["project_task_ids"], status=input_data["status"], updated_by=input_data.get("updated_by", None))
#         return generate_response(message="Status updated!", status= HTTP_200_OK)
#     except Exception as e:
#         return generate_response(message=e, status=HTTP_400_BAD_REQUEST)
    





    


