from app.db import get_db_conn
from app.utils.common import generate_response, TokenGenerator
from datetime import datetime, timezone, timedelta
from flask import jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
# from users.helper import send_forgot_password_email

import psycopg2.extras



class Project():
    def __init__(self):
        self.db= get_db_conn()


    def get_my_projects(self, email):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        curs.execute(f"""
        SELECT p.* FROM projectmaster p, projecttaskmaster pt
        WHERE pt.assigneeemail = \'{email}\' AND pt.projectid=p.projectid
""")
        
        projects = curs.fetchall()
        curs.close()
        # return [project for project in projects]
        return jsonify(projects)
    
    def get_project_info(self, project_id):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        curs.execute(f"""
            SELECT pt.* FROM projecttaskmaster pt
            WHERE pt.projectid = \'{project_id}\'
            """)
        
        project_info= curs.fetchall()
        return jsonify(project_info)

    