from flask import current_app as app
from flask.globals import request
from cpdservice.utils.resource import Resource
from cpdservice.service_api_handlers import ( get_recieved_orders_handler,
                                             post_recieved_orders_handler, 
                                             put_recieved_orders_handler )



class Manage_Orders(Resource):
    
    def get(self):
        
        status=str(request.args.get('status'))
        return get_recieved_orders_handler.handle_request(status) 
        
    def put(self):
        request_data = request.get_json(force=True)
        orderId = request_data.get('order_id')
        status=str(request_data.get('status'))
        return put_recieved_orders_handler.handle_request(orderId, status)
    
    def post(self):
        
        request_data = request.get_json(force=True)
        orderId = request_data.get('order_id')
        print orderId
        status=str(request_data.get('status'))
        if 'docket_no' in request_data:
            docket_no = request_data.get('docket_no')
            return post_recieved_orders_handler.handle_returned_request(orderId, status, docket_no)
        else:
            return post_recieved_orders_handler.handle_delivered_request(orderId, status)