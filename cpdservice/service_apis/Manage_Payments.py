from flask import current_app as app
from flask.globals import request
from cpdservice.utils.resource import Resource
from DBLayer.order_management.models import Order
from cpdservice.service_api_handlers import ( get_payments_handler,
                                              post_payments_handler )

class Manage_Payments(Resource):
    
    def get(self):
        status = str(request.args.get('status'))
        return get_payments_handler.handle_request(status)
    
    def post(self):
        request_data = request.get_json(force=True)
        return post_payments_handler.handle_payment_request(request_data)
        

