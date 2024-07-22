from app.db import get_db_conn
from app.utils.common import generate_response, TokenGenerator
from datetime import datetime, timezone, timedelta
from flask import jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
# from users.helper import send_forgot_password_email
import psycopg2.extras


class Dashboard():
    def __init__(self):
        self.db= get_db_conn()

    
    def get_open_tasks(self, employee_id):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # TODO #add dependency tasks 
        curs.execute(
            f""" SELECT pt.*, tm.taskname, pm.projectname FROM projecttaskmaster pt, taskmaster tm, projectmaster pm
            WHERE pt.assigneeemail = \'{employee_id}\' AND pt.completion IS FALSE AND pt.taskid =  tm.taskid AND pt.projectid = pm.projectid
""")
        open_tasks= curs.fetchall()

        column_names = [desc[0] for desc in curs.description]
        curs.close()

        result = [dict(zip(column_names, row)) for row in open_tasks]
        return (result)

    
    def get_closed_tasks(self, employee_id):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curs.execute(
            f""" SELECT pt.*, tm.taskname, pm.projectname FROM projecttaskmaster pt, taskmaster tm, projectmaster pm
            WHERE pt.assigneeemail = \'{employee_id}\' AND pt.completion IS TRUE AND pt.taskid =  tm.taskid AND pt.projectid = pm.projectid
            
""")
        closed_tasks= curs.fetchall()
        column_names = [desc[0] for desc in curs.description]
        curs.close()
        result = [dict(zip(column_names, row)) for row in closed_tasks]
        return (result)
        # return [task for task in closed_tasks]
         
    
    def change_status(self, employee_id:str, project_task_id:str, status:bool):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        curs.execute(
            f"""
            UPDATE projecttaskmaster p SET completion = {status}
            WHERE p.projecttaskid = {project_task_id} AND p.assigneeemail = \'{employee_id}\';
""")
        # curs.fetchall()
        self.db.commit()
        curs.close()
        self.db.close()
        return True
    
# dashboard = Dashboard()
