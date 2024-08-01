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


# @home.route("/change_task_status", methods=["POST"])
# @cross_origin()
# def change_task_status():
#     input_data =request.get_json()

#     try:
#         Dashboard().change_status(employee_id=input_data["email"], project_task_id=input_data["project_task_id"], status=input_data["status"], updated_by=input_data.get("updated_by", None))
#         return generate_response(message="Status updated!", status= HTTP_200_OK)
#     except Exception as e:
#         return generate_response(message=e, status=HTTP_400_BAD_REQUEST)

    

# @home.route("/change_task_status", methods=["POST"])
# @cross_origin()
# def change_task_status():
#         data = request.get_json()
#         emails = data['email']
#         project_task_ids = data['project_task_id']
#         statuses = data['status']
#         print(emails, project_task_ids, statuses)
#         try:
#             for email, project_task_id, status in zip(emails, project_task_ids, statuses):
#                 # print(email, project_task_id, status)
#                 Dashboard().change_status(employee_id=email, project_task_id=project_task_id, status=status, updated_by=data.get("updated_by", None))
#             return generate_response(message="Status updated!", status= HTTP_200_OK)
#         except Exception as e:
#             return generate_response(message=str(e), status=HTTP_400_BAD_REQUEST)
# @home.route("/change_task_status", methods=["POST"])
# @cross_origin()
# def change_task_status():
#     tasks = request.get_json()
#     try:
#         for task in tasks:
#             Dashboard().change_status(employee_id=task["email"], project_task_id=task["project_task_id"], status=task["status"], updated_by=task.get("updated_by", None))
#         print(task)

#         return generate_response(message="Status updated!", status= HTTP_200_OK)
#     except Exception as e:
#         return generate_response(message=str(e), status=HTTP_400_BAD_REQUEST)

@home.route("/change_task_status", methods=["POST"])
@cross_origin()
def change_task_status():
    try:
        data_list = request.get_json()
        print(f"Received data: {data_list}")  
        update_results = []


        for data in data_list:
            email = data.get('email')
            project_task_id = data.get('project_task_id')
            status = data.get('status')
            updated_by = data.get('updated_by', email) 
            print(f"Processing: {email}, {project_task_id}, {status}, {updated_by}")


            # Ensure all necessary fields are provided
            if not (email and project_task_id and status is not None):
                return jsonify({"message": "Missing required fields"}), 400
            # print(email, project_task_id, status, updated_by)


            # Change the status for the single task
            result = Dashboard().change_status(
                employee_id=email,
                project_task_ids=[project_task_id],  # Passing a single task ID as a list
                status=status,
                updated_by=updated_by
            )

            if not result:
                print(f"Failed to update task status for: {email}, {project_task_id}")
                update_results.append({"email": email, "project_task_id": project_task_id, "status": "failed"})
            else:
                update_results.append({"email": email, "project_task_id": project_task_id, "status": "success"})
        return jsonify({"message": "Status updated!", "results": update_results}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400





    


