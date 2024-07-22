from app.db import get_db_conn
from app.utils.common import generate_response, TokenGenerator
from datetime import datetime, timezone, timedelta
from flask import jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
# from users.helper import send_forgot_password_email
import psycopg2.extras


class Summary():
    def __init__(self):
        self.db=get_db_conn()

    def get_open_tasks_count(self, email):
        curs =self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curs.execute(
            f""" 
            SELECT COUNT(pt.projecttaskid) AS open_tasks_count FROM projecttaskmaster pt
            WHERE pt.assigneeemail = \'{email}\' AND pt.completion IS FALSE;
""")
        open_tasks_count = curs.fetchall()
        column_names = [desc[0] for desc in curs.description]
        curs.close()

        result = [dict(zip(column_names, row)) for row in open_tasks_count]
        return (result)


    def get_closed_tasks_count(self, email):
        curs =self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curs.execute(
            f""" 
            SELECT COUNT(pt.projecttaskid) AS closed_tasks_count FROM projecttaskmaster pt
            WHERE pt.assigneeemail = \'{email}\' AND pt.completion IS TRUE;
""")
        closed_tasks_count = curs.fetchall()
        column_names = [desc[0] for desc in curs.description]
        curs.close()

        result = [dict(zip(column_names, row)) for row in closed_tasks_count]
        return (result)
    
    def get_overdue_tasks_count(self,email):
        curs =self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curs.execute(
            f""" 
            SELECT COUNT(pt.projecttaskid) AS overdue_tasks_count FROM projecttaskmaster pt
            WHERE pt.assigneeemail = \'{email}\' AND pt.completion IS FALSE AND pt.duedate< CURRENT_DATE;
""")
        overdue_tasks_count = curs.fetchall()
        column_names = [desc[0] for desc in curs.description]
        curs.close()

        result = [dict(zip(column_names, row)) for row in overdue_tasks_count]
        return (result)
    
    def get_project_count(self, email):
        curs =self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curs.execute(
            f""" 
            SELECT COUNT(DISTINCT pt.projectid) AS project_count FROM projecttaskmaster pt
            WHERE pt.assigneeemail = \'{email}\' AND pt.completion IS FALSE;
""")
        project_count = curs.fetchall()
        column_names = [desc[0] for desc in curs.description]
        curs.close()

        result=[dict(zip(column_names, row)) for row in project_count]
        return result



    def get_summary(self, email_id):
        
        open_tasks_count = self.get_open_tasks_count(email=email_id)

        closed_tasks_count = self.get_closed_tasks_count(email=email_id)

        overdue_tasks_count = self.get_overdue_tasks_count(email=email_id)

        project_count = self.get_project_count(email=email_id)

        summary = {**open_tasks_count[0], **closed_tasks_count[0], **overdue_tasks_count[0], **project_count[0]}

        return jsonify(summary)