from flask import Blueprint,request,  jsonify
from app.crud.summary import Summary
from app.utils.common import generate_response
from app.utils.http_code import *
from flask_cors import cross_origin
# from app.endpoints.api import main


summary = Blueprint('summary', __name__)
@summary.route("/get_summary", methods=['GET'])
@cross_origin()
def get_summary():
    try :
        email = request.args.get('email_id')
        
        summary = Summary().get_summary(email_id=email)
        return summary
    except Exception as e :
        return generate_response(status =400, message ="Some error occured while getting the summary." ) 