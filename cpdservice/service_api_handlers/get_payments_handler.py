from DBLayer.order_management.models import Order
from DBLayer.cpd.models import Incentive
from DBLayer.inventory.models import Delivery
from DBLayer.cpd.models import Channel_Partner
from cpdservice.utils.auth import get_user

def handle_request(status):
    response=[]
    current_user = Channel_Partner.objects.get(executive=get_user()).name
    delivery_obj = Delivery.objects.filter(order__status=str(status),to_channel_partner=str(current_user))
    for delivery in delivery_obj:
            order_dict={}
            order_dict['order_id'] = delivery.order.sales_order_id
            order_dict['firstname'] = delivery.order.owner.first_name.title()
            order_dict['middlename'] = delivery.order.owner.middle_name.title()
            order_dict['lastname'] = delivery.order.owner.last_name.title()
            order_dict['amount'] = delivery.order.grand_total
            order_dict['incentive'] = Incentive.objects.get(delivery=Delivery.objects.get(order=delivery.order)).incentive
            response.append(order_dict)
    return response