from DBLayer.order_management.models import OrderItem
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
            order_dict['taluka'] = delivery.order.billing_address.taluka
            order_dict['village'] = delivery.order.billing_address.village
            order_dict['postoffice'] = delivery.order.billing_address.post_office
            order_dict['district'] = delivery.order.billing_address.district
            order_dict['street'] = delivery.order.billing_address.street
            order_dict['pincode'] = delivery.order.billing_address.pin_code
            order_dict['created_date'] = (delivery.order.created_on).strftime("%d/%m/%Y")
            order_items = OrderItem.objects.filter(order=delivery.order)
            orderItemList=[]
            order_qty_list=[]
            for oi in order_items:
                orderitem = oi.item_name.split('-')
                orderItemList.append(orderitem[1])
                order_qty_list.append(oi.quantity)
            order_dict['orderitems']=orderItemList
            order_dict['orderitem_quantity']=order_qty_list
            order_dict['total_price'] = delivery.order.cod_amount
            order_dict['mobile_no'] = delivery.order.notification_mobile
            response.append(order_dict)
    return response

