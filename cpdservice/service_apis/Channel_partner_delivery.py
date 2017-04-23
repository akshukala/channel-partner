from flask import current_app as app
from flask.globals import request
from cpdservice.utils.resource import Resource
from DBLayer.order_management.models import Order
from cpdservice.service_api_handlers import get_channel_partner_delivery_handler



class Channel_partner_delivery(Resource):
    
    def get(self):
        
        if 'docket_no' in request.args:
            data = request.args
            docket_no = data['docket_no']
            return get_channel_partner_delivery_handler.handle_request(docket_no)
        else:    
            return get_channel_partner_delivery_handler.handle_incoming_package_request()
    
    def put(self):
        request_data = request.get_json(force=True)
        order_id = int(request_data.get('order_id'))
        order_obj = Order.objects.get(sales_order_id=order_id)
        order_obj.status = str(request_data.get('status'))
        order_obj.save()
        return "Status successfully updated"     
    
    