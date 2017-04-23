from flask import current_app as app
from flask.globals import request
from cpdservice.utils.resource import Resource
from cpdservice.service_api_handlers import Channel_partner_summary_handler


class Channel_partner_summary(Resource):
    
    def get(self):
        
        return Channel_partner_summary_handler.handle_request()
