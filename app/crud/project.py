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
        SELECT DISTINCT p.* FROM projectmaster p, projecttaskmaster pt
        WHERE pt.assigneeemail = \'{email}\' AND pt.projectid=p.projectid
""")
        
        projects = curs.fetchall()
        # return projects

        column_names = [desc[0] for desc in curs.description]
        curs.close()

        result = [dict(zip(column_names, row)) for row in projects]
        
        return jsonify(result)
    
    def get_project_info(self, project_id):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        curs.execute(f"""
            SELECT 
                um.email AS assignee,
                pt.completion,
                pt.specialinstruction,
                pt.exception,
                tm.taskname,
                fm.functionname AS function 
            
            FROM 
                projecttaskmaster pt,
                taskmaster tm,
                usermaster um,
                functionmaster fm
            
            WHERE 
                pt.projectid = \'{project_id}\' AND 
                pt.taskid = tm.taskid AND 
                pt.assigneeemail= um.email AND 
                pt.functionid=fm.functionid
            """)
        
        project_info= curs.fetchall()

        column_names = [desc[0] for desc in curs.description]
        curs.close()

        result = [dict(zip(column_names, row)) for row in project_info]


        return jsonify(result)

    