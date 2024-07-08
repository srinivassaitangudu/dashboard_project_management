from app.db import get_db_conn
from datetime import datetime, timezone, timedelta
from flask_bcrypt import generate_password_hash, check_password_hash
# from users.helper import send_forgot_password_email
from app.utils.common import generate_response, TokenGenerator
import psycopg2.extras



class Dashboard():
    def __init__(self):
        self.db= get_db_conn()

    
    def get_open_tasks(self, employee_id):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        curs.execute(
            f""" SELECT * FROM projecttaskmaster P
            WHERE P.assignee = \'{employee_id}\' AND P.completion IS FALSE
""")
        open_tasks= curs.fetchall()
        curs.close()
        return [task for task in open_tasks]

    
    def get_closed_tasks(self, employee_id):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curs.execute(
            f""" SELECT * FROM projecttaskmaster P
            WHERE P.assignee = \'{employee_id}\' AND P.completion IS TRUE
            LIMIT 5
""")
        closed_tasks= curs.fetchall()
        curs.close()
        return [task for task in closed_tasks]
         
    
    def change_status(self, employee_id:str, project_task_id:str, status:bool):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        curs.execute(
            f"""
            UPDATE projecttaskmaster p SET completion = {status}
            WHERE p.projecttaskid = {project_task_id} AND p.assignee = \'{employee_id}\';
""")
        # curs.fetchall()
        self.db.commit()
        curs.close()
        return True
    
# dashboard = Dashboard()
