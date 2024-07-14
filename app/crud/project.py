from app.db import get_db_conn
from datetime import datetime, timezone, timedelta
from flask_bcrypt import generate_password_hash, check_password_hash
# from users.helper import send_forgot_password_email
from app.utils.common import generate_response, TokenGenerator
import psycopg2.extras



class Project():
    def __init__(self):
        self.db= get_db_conn()


    def get_my_projects(self, email):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        curs.exceute(f"""
        SELECT p.* FROM projectmaster p, projecttaskmaster pt
        WHERE pt.assignee = \'{email}\' AND pt.projectid=p.projectid
""")
        
        projects = curs.fetchall()
        return projects
    
    def get_project_info(self, project_id):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        curs.execute(f"""
            SELECT pt.* FROM projecttaskmaster pt
            WHERE pt.project_id = \'{project_id}\'
            """)
        
        project_info= curs.fetchall()
        return project_info

    