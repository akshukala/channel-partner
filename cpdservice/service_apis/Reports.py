import json
import os
from os.path import dirname
from flask import current_app as app
from flask.ext.restful import Resource
from cpdservice.reports import reports_handler
from flask import request, send_file
from datetime import datetime

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
            os.makedirs(dir)

class Reports(Resource):
    
    def get(self):
        request_data = json.loads([k for k in request.args.to_dict()][0])
        report_type = request_data.get('type')
        from_date = request_data.get('from_date')
        to_date = request_data.get('to_date')
        user_id = request_data.get('userId')
        UPLOAD_FOLDER = os.path.join(dirname(app.root_dir), 'Documents')
        
        if report_type == 'Order Report':
            
            filename = "Orders_report" + datetime.now().isoformat() + ".csv"
            file_name = os.path.join(UPLOAD_FOLDER,filename)
            assure_path_exists(file_name)
            reports_handler.create_order_csv(file_name, from_date, to_date, user_id)
            return send_file(file_name, attachment_filename='Order_Report.csv', as_attachment=True)
        else:
            filename = "Transcation_report" + datetime.now().isoformat() + ".csv"
            file_name = os.path.join(UPLOAD_FOLDER,filename)
            assure_path_exists(file_name)
            reports_handler.create_transaction_csv(file_name, from_date, to_date, user_id)
            return send_file(file_name, attachment_filename='Transaction_Report.csv', as_attachment=True)
       
    get.authenticated = False