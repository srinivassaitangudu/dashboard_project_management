from db import get_db_conn
from datetime import datetime, timezone, timedelta
from flask_bcrypt import generate_password_hash, check_password_hash
# from users.helper import send_forgot_password_email
from utils.common import generate_response, TokenGenerator
import psycopg2.extras



class Dashboard():
    def __init__(self):
        self.db= get_db_conn()

    
    def get_open_tasks(self, employee_id):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return

    
    def get_closed_tasks(self, employee_id):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return 
    
    def change_status(self, employee_id:str, task_id:str):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return 
