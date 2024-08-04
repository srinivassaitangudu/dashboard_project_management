from flask import Blueprint, app, logging,request,  jsonify
from app.crud import dashboard
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
    try:
        data_list = request.get_json()
        print(f"Received data: {data_list}")  
        update_results = []


        for data in data_list:
            try:
                email = data.get('email')
                project_task_id = data.get('project_task_id')
                status = data.get('status')
                print(f"Processing: {email}, {project_task_id}, {status}")

                if not (email and project_task_id and status is not None):
                    print("Missing required fields")
                    return jsonify({"message": "Missing required fields"}), 400

                result = Dashboard().change_status(
                    employee_id=email,
                    project_task_ids=[project_task_id],  
                    status=status
                )

                if not result:
                    print(f"Failed to update task status for: {email}, {project_task_id}")
                    update_results.append({"email": email, "project_task_id": project_task_id, "status": "failed"})
                else:
                    update_results.append({"email": email, "project_task_id": project_task_id, "status": "success"})
            
            except Exception as e:
                print(f"Exception while processing item: {e}")
                update_results.append({"email": email, "project_task_id": project_task_id, "status": "exception", "message": str(e)})

        
        
        print(f"Update results: {update_results}")  # New print statement
        return jsonify({"message": "Status updated!", "results": update_results}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400