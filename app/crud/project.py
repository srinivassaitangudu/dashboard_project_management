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


    def get_all_projects(self):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        curs.execute(f"""
        SELECT DISTINCT p.* FROM projectmaster p;
""")
        
        projects = curs.fetchall()
    
        column_names = [desc[0] for desc in curs.description]
        curs.close()

        result = [dict(zip(column_names, row)) for row in projects]
        
        return jsonify(result), 200
    
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
    
    def get_create_task_info(self, project_id):

        task_info = self.get_task_list(project_id=project_id)
        assignee_info = self.get_assignee_list()
        function_list = self.get_function_list()


        return {**task_info, **assignee_info, **function_list}
    
    def get_assignee_list(self):

        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curs.execute(
        """
        SELECT um.email, um.name FROM usermaster um;
        """
        )
        assignee_info = curs.fetchall()
        column_names = [desc[0] for desc in curs.description]
        curs.close()

        result = [dict(zip(column_names, row)) for row in assignee_info]

        return ({"assignees":result})
    
    def get_task_list(self, project_id):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curs.execute(
            f"""
            SELECT tm.* FROM  taskmaster tm

            WHERE tm.taskid NOT IN  (SELECT ptm.taskid FROM projecttaskmaster ptm WHERE ptm.projectid =\'{project_id}\')
"""
        )
        task_info = curs.fetchall()
        column_names = [desc[0] for desc in curs.description]
        curs.close()

        result = [dict(zip(column_names,row)) for row in task_info]
        return ({"tasks":result})
    
    def get_function_list(self):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curs.execute(
            """
            SELECT * FROM functionmaster"""
        )
        function_info = curs.fetchall()
        column_names = [desc[0] for desc in curs.description]
        curs.close()

        result = [dict(zip(column_names,row)) for row in function_info]
        return ({"functions":result})
    
    def create_new_task(self, taskname:str):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        curs.execute("""
            INSERT INTO taskmaster (taskname, functionid, weightage)
            VALUES (%s, %s, %s) RETURNING taskid
""", [taskname,'', None])
        
        taskid = curs.fetchone()
        self.db.commit()
        curs.close()

        return taskid
    
    def add_new_task_to_project(self, task_id, project_id, function_id, assigneeemail, exception, special_instruction, weightage, duedate, createdby ):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # curs.execute(
        #     """
        #     INSERT INTO projecttaskmaster 
        #     (
        #     projectid, taskid, assigneeemail, functionid, completion, exception, specialinstruction, weightage, priority, duedate, createdby, createdon, lastupdatedby, lastupdatedon, dependencyoveride, active) 
        #     VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s) RETURNING projecttaskid
        #     """, [project_id, task_id, assigneeemail, function_id, False, exception, special_instruction, str(weightage), '', duedate, createdby,  str(datetime.now(timezone.utc)), None, None, False, True ])
        curs.execute(
        f"""
            INSERT INTO projecttaskmaster 
            (
            projectid, taskid, assigneeemail, functionid, completion, exception, specialinstruction, weightage, priority, duedate, createdby, createdon, lastupdatedby, lastupdatedon, dependencyoverride, active) 
            VALUES (\'{project_id}\', \'{task_id}\',\'{assigneeemail}\', \'{function_id}\',false,\' {exception}\',\'{special_instruction}\', {weightage},NULL, \'{duedate}\',\'{createdby}\', \'{datetime.now(timezone.utc).date()}\',NULL, NULL, false, true) RETURNING projecttaskid ;
            """)
        
        project_task_id =curs.fetchone()
        self.db.commit()
        # curs.commit()
        curs.close()

        return project_task_id
    
    def delete_task_in_project(self, project_task_id):
        curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curs.execute(f"""
            DELETE * FROM projecttaskmaster ptm
            WHERE ptm.projecttaskid =\'{project_task_id}\'
            RETURNING ptm.projecttaskid;""")
        project_task_id = curs.fetchone()
        self.db.commit()
        curs.close()
        return project_task_id














    