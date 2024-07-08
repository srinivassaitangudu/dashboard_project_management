from flask import Blueprint,request,  jsonify
from app.crud.dashboard import Dashboard

main = Blueprint('main', __name__)

@main.route("/health", methods=['GET'])
def health_check():
    return jsonify({"status": "UP"}), 200

@main.route("/open_tasks", methods=["GET"])
def get_open_tasks():
    email = request.args.get('email')

    open_tasks = Dashboard().get_open_tasks(employee_id=email)

    return jsonify({'open_tasks':open_tasks})

@main.route("/closed_tasks", methods=["GET"])
def get_closed_tasks():
    email = request.args.get('email')

    closed_tasks = Dashboard().get_closed_tasks(employee_id=email)
    return jsonify({"closed_tasks":closed_tasks})


@main.route("/change_task_status", methods=["POST"])
def change_task_status():
    input_data =request.json
    Dashboard().change_status(employee_id=input_data["email"], project_task_id=input_data["project_task_id"], status=input_data["status"])



    


