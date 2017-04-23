from django.contrib.auth.models import User
from django.db.models import Count
from cpdservice.utils.auth import get_user
from DBLayer.inventory.models import Delivery
from DBLayer.order_management.models import OrderItem
from DBLayer.cpd.models import Channel_Partner


def handle_request(docket_no):
    response = []
    delivery_objs = Delivery.objects.filter(delivery_chalan=str(docket_no),delivery_by='Channel Partner')
    
    for delivery_obj in delivery_objs:
        if(delivery_obj.order.status=="DISPATCHED"):
            delivery_dict = {}
            delivery_dict['order_id'] = delivery_obj.order.sales_order_id
            orderItemList=[]
            order_items = OrderItem.objects.filter(order=delivery_obj.order.sales_order_id)
            for oi in order_items:
                orderitem = oi.item_name.split('-')
                orderItemList.append(orderitem[1])
            delivery_dict['orderitems']=orderItemList
            response.append(delivery_dict)
        else:
            pass
    return response
    
    
def handle_incoming_package_request():
    user_id = get_user().id
    channel_partner_name = Channel_Partner.objects.get(executive=User.objects.get(id=user_id)).name
    packages_count = Delivery.objects.filter(to_channel_partner=str(channel_partner_name),order__status='DISPATCHED')\
            .values('delivery_chalan')\
            .annotate(package_order_count = Count('delivery_chalan'))
    packages = list(packages_count)
    return packages