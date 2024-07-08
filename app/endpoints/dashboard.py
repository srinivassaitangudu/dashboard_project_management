from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route("/health", methods=['GET'])
def health_check():
    return jsonify({"status": "UP"}), 200

@main.route("/open_tasks/", methods=["GET"])
def get_open_tasks(employee_id:str):

    return jsonify({'open_tasks':employee_id})

@main.route("/closed_tasks")
def get_closed_tasks(employee_id:str):
    return jsonify({"closed_tasks":employee_id})
