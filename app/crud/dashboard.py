from app.db import get_db_conn
from app.utils.common import generate_response, TokenGenerator
from datetime import datetime, timezone, timedelta
from flask import jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from typing import List
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
         
    
#     def change_status(self, employee_id:str, project_task_id:str, status:bool, updated_by:str):
#         curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

#         curs.execute(
#             f"""
#             UPDATE projecttaskmaster p SET 
#             completion = {status},
#             lastupdatedon= \'{datetime.now(timezone.utc).date()}\',
#             lastupdatedby= \'{employee_id}\'

#             WHERE p.projecttaskid = \'{project_task_id}\';
# """)
#         # curs.fetchall()
#         self.db.commit()
#         curs.close()
#         self.db.close()
#         return True
    def change_status(self, employee_id:str, project_task_ids:List[str], status:str, updated_by:str):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # Convert status to appropriate database value
        status_value = 1 if status.lower() == 'completed' else 0

        if not project_task_ids:
                raise ValueError("No project task IDs provided")

        # Convert list of IDs to a format suitable for SQL IN clause
        task_ids_str = ', '.join(f"'{task_id}'" for task_id in project_task_ids)

        curs.execute(
            f"""
            UPDATE projecttaskmaster p SET 
            completion = {status_value},
            lastupdatedon= \'{datetime.now(timezone.utc).date()}\',
            lastupdatedby= \'{employee_id}\'

            WHERE p.projecttaskid IN ({task_ids_str});
        """)
        self.db.commit()
        curs.close()
        self.db.close()
        return True
    
# dashboard = Dashboard()
