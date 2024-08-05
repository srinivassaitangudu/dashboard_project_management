from app.db import get_db_conn
from app.utils.common import generate_response, TokenGenerator
from collections import defaultdict
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
    
    # def get_project_info(self, project_id):
    #     curs = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    #     curs.execute(f"""
    #         SELECT 
    #             um.email AS assignee,
    #             pt.projectid,
    #             pt.completion,
    #             pt.specialinstruction,
    #             pt.exception,
    #             tm.taskname,
    #             fm.functionname AS function,
    #             fm.functionid
                      
            
    #         FROM 
    #             projecttaskmaster pt,
    #             taskmaster tm,
    #             usermaster um,
    #             functionmaster fm
            
    #         WHERE 
    #             pt.projectid = \'{project_id}\' AND 
    #             pt.taskid = tm.taskid AND 
    #             pt.assigneeemail= um.email AND 
    #             pt.functionid=fm.functionid
    #         """)
        
    #     project_info= curs.fetchall()

    #     column_names = [desc[0] for desc in curs.description]
    #     curs.close()

    #     result = [dict(zip(column_names, row)) for row in project_info]
    #     return jsonify(result)
    
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
    

    def get_project_info(self, projectid):

        project_info = self.get_project_meta_info(projectid=projectid)
        project_info["readinessscore"] *=100
        project_info["readinessscore"] = f"{project_info['readinessscore']:.2f}"


        raw_project_functions_info = self.get_project_functions_info(projectid=projectid)
        formatted_project_functions_info = self.groupby_function_info(function_info=raw_project_functions_info)
        
        project_info["functions_info"] = formatted_project_functions_info
        return project_info
    

    def get_project_meta_info(self, projectid):

        curs=self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        curs.execute(
            f"""
            SELECT pm.*, pv.readinessscore
            FROM projectmaster pm
            INNER JOIN projectreadinessscoreview pv ON pv.projectid = pm.projectid
            WHERE pm.projectid = \'{projectid}\'""")
        project_info = curs.fetchall()
        column_names = [desc[0] for desc in curs.description]
        curs.close()
        # self.db.close()
        result = [dict(zip(column_names, row)) for row in project_info]
        return result[0]
    
    def get_project_functions_info(self, projectid):
        curs=self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curs.execute(f"""
    SELECT 
                    ptm.*,
                    pfv.readinessscore AS functionreadinessscore,
                    pfm.functionleademail,
                    um1.email AS assigneeemail,
                    um1.name AS assigneename, 
                    um2.name AS functionleadname,
                    tm.taskname,
                    fm.functionname
                     
            FROM projecttaskmaster ptm
            JOIN projectfunctionmaster pfm ON (pfm.projectid =ptm.projectid AND pfm.functionid = ptm.functionid)
            JOIN taskmaster tm ON tm.taskid = ptm.taskid
            JOIN projectfunctionreadinessscoreview pfv 
                     ON 
                     (pfv.projectid=ptm.projectid AND ptm.functionid=pfv.functionid)
                     
            INNER JOIN usermaster um1 ON um1.email = ptm.assigneeemail
            INNER JOIN usermaster um2 ON um2.email = pfm.functionleademail
            INNER JOIN functionmaster fm ON fm.functionid = ptm.functionid
            WHERE ptm.projectid = \'{projectid}\'
            """)
        function_info =curs.fetchall()
        column_names = [desc[0] for desc in curs.description]
        curs.close()
        # self.db.close()
        result = [dict(zip(column_names, row)) for row in function_info]
        return result

    def groupby_function_info(self, function_info):

        grouped_data = defaultdict(lambda: {
                "functionid": "",
                "functionname": "",
                "functionreadinessscore": "",
                "functionleademail": "",
                "functionleadname": "",
                "tasks": []
            })
        
        for item in function_info:
            functionid = item["functionid"]

            # Populate the main dictionary structure
            grouped_data[functionid]['functionid'] = item['functionid']
            grouped_data[functionid]['functionname'] = item['functionname']
            grouped_data[functionid]['functionreadinessscore'] = item['functionreadinessscore']*100
            grouped_data[functionid]['functionreadinessscore'] = "{:.2f}".format(grouped_data[functionid]['functionreadinessscore'])
            grouped_data[functionid]['functionleademail'] = item['functionleademail']
            grouped_data[functionid]['functionleadname'] = item['functionleadname']
        
            
            # Add the task details to the "tasks" list
            task_details = {
                "projecttaskid": item['projecttaskid'],
                "taskname": item['taskname'],
                "assigneename": item['assigneename'],
                "assigneeemail": item['assigneeemail'],
                "completion": item['completion'],
                "weightage": item["weightage"],
                "createdby" : item["createdby"],
                "createdon" : item["createdon"],
                "lastupdatedby":item["lastupdatedby"],
                "lastupdatedon":item["lastupdatedon"],
                "duedate":item["duedate"],
                'exception': item["exception"],
                'specialinstruction': item["specialinstruction"]   
            }
            grouped_data[functionid]['tasks'].append(task_details)
        
        # Convert the defaultdict to a list of dicts
        formatted_data = list(grouped_data.values())
        return formatted_data

    def change_assignee(self, task_and_assignee_info):
        curs=self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        curs.execute(f"""
            UPDATE projecttaskmaster 
            SET 
            assigneeemail =\'{task_and_assignee_info["assigneeemail"]}\',
            lastupdatedby =\'{task_and_assignee_info["email"]}\',
            lastupdatedon = \'{datetime.now(timezone.utc)}\'
            WHERE projecttaskid =\'{task_and_assignee_info["projecttaskid"]}\'; """)
        
        self.db.commit()
        curs.close()
        # self.db.close()
        return True


        




        














    