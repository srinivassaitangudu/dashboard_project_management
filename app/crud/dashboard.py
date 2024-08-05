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
            f""" select pt.* , t.taskname,f.functionname, pm.projectname,u.name,coalesce(cu.name,'') as createdbyName, coalesce(lu.name,'') as lastupdatebyName
from projecttaskmaster pt
inner join taskmaster t on t.taskid =pt.taskid 
inner join functionmaster f on f.functionid=t.functionid
inner join projectmaster pm on pm.projectid =pt.projectid 
inner join usermaster u on pt.assigneeemail = u.email 
left join usermaster cu on pt.createdby = cu.email 
left join usermaster lu on pt.lastupdatedby = lu.email
where pt.assigneeemail = \'{employee_id}\'
and pt.completion is false 
order by CASE 
        WHEN pt.duedate IS NULL THEN 1 
        ELSE 0 
    END,
    pt.duedate
""")
        open_tasks= curs.fetchall()

        column_names = [desc[0] for desc in curs.description]
        curs.close()

        result = [dict(zip(column_names, row)) for row in open_tasks]
        return (result)

    
    def get_closed_tasks(self, employee_id):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curs.execute(
            f""" select pt.* , t.taskname,f.functionname, pm.projectname,u.name,coalesce(cu.name,'') as createdbyName, coalesce(lu.name,'') as lastupdatebyName
from projecttaskmaster pt
inner join taskmaster t on t.taskid =pt.taskid 
inner join functionmaster f on f.functionid=t.functionid
inner join projectmaster pm on pm.projectid =pt.projectid 
inner join usermaster u on pt.assigneeemail = u.email 
left join usermaster cu on pt.createdby = cu.email 
left join usermaster lu on pt.lastupdatedby = lu.email
where pt.assigneeemail = \'{employee_id}\'
and pt.completion is True 
order by pt.lastupdatedon desc
            
""")
        closed_tasks= curs.fetchall()
        column_names = [desc[0] for desc in curs.description]
        curs.close()
        result = [dict(zip(column_names, row)) for row in closed_tasks]
        return (result)
        # return [task for task in closed_tasks]
         


    def change_status(self, employee_id:str, project_task_ids:List[str], status:bool):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
     
        if not project_task_ids:
                raise ValueError("No project task IDs provided")

        task_ids_str = ', '.join(f"'{task_id}'" for task_id in project_task_ids)
        # print("HEREEEEEE", project_task_ids, status, employee_id)


        curs.execute(
            f"""
            UPDATE projecttaskmaster p SET 
            completion = {status},
            lastupdatedon= \'{datetime.now(timezone.utc).date()}\'
            WHERE p.projecttaskid IN ({task_ids_str});
            """)

        self.db.commit()
        curs.close()
        self.db.close()
        return True
    
   
    
# dashboard = Dashboard()
