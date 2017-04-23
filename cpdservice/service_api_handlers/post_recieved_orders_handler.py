from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import math
from cpdservice.utils.auth import get_user
from DBLayer.inventory.models import Delivery,Return_Delivery
from DBLayer.order_management.models import Order
from DBLayer.cpd.models import Payment,Incentive,Channel_Partner,IncentiveStructure

def handle_delivered_request(orderId,status):
    
    delivery = Delivery.objects.get(order=Order.objects.get(sales_order_id=orderId))
    try:
        payment_exists = Payment.objects.get(delivery=delivery)
    except ObjectDoesNotExist:
        payment_exists = None
    if payment_exists:
        return {"errorCode":"400",
                 "errorMessage":"Payment already recieved"}
    '''Changing order status'''
    order_obj = Order.objects.get(sales_order_id=delivery.order.sales_order_id)
    order_obj.status=str(status)
    order_obj.save()
    
    '''Creating Payment Object'''
    Payment.objects.create(delivery=delivery,cash_collected=delivery.order.grand_total)
    '''Calculating Incentive'''
    weight = int(delivery.total_weight)
    if weight <= 2000:
        incentive = 120
    else:
        reduced_wt = float(weight - 2000)
        wt_in_kg = reduced_wt/1000
        final_reduced_wt=round(wt_in_kg) + 2
        
        try:
            incentive = IncentiveStructure.objects.get(weight_greater_than_equal=int(final_reduced_wt)).incentive
        except ObjectDoesNotExist: 
            incentive = 120 + 15*final_reduced_wt 
    Incentive.objects.create(delivery=delivery,incentive=incentive)    
    return "Success"

def handle_returned_request(orderId, status, docket_no):
    
    for itr in range(0,len(orderId)):
        delivery = Delivery.objects.get(order=Order.objects.get(sales_order_id=orderId[itr]))
        order_obj = Order.objects.get(sales_order_id=delivery.order.sales_order_id)     
        order_obj.status=str(status)
        order_obj.save()
        '''Calculating Incentive'''
        weight = int(delivery.total_weight)
        if weight <= 2000:
            incentive = 120
        else:
            reduced_wt = float(weight - 2000)
            wt_in_kg = reduced_wt/1000
            final_reduced_wt=round(wt_in_kg) + 2        
            try:
                incentive = IncentiveStructure.objects.get(weight_greater_than_equal=int(final_reduced_wt)).incentive
            except ObjectDoesNotExist: 
                incentive = 120 + 15*final_reduced_wt    
        Incentive.objects.create(delivery=delivery,incentive=(incentive/2))
        '''Creating Return Delivery Object'''
        user_id = get_user().id
        channel_partner_name = Channel_Partner.objects.get(executive=User.objects.get(id=user_id)).name
        Return_Delivery.objects.create(order=order_obj,delivery_chalan=str(docket_no),from_channel_partner=channel_partner_name) 
    return "Success"


