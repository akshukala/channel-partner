from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from cpdservice.utils.auth import get_user
from DBLayer.inventory.models import Delivery
from DBLayer.order_management.models import Order
from DBLayer.cpd.models import Payment,Incentive,Channel_Partner,Transaction,KrishiexAccount

def handle_payment_request(request_data):
    
    order_ids = request_data.get('order_id')
    user_id = get_user().id
    channel_partner_obj = Channel_Partner.objects.get(executive=User.objects.get(id=user_id))
    krichiex_acc_obj= KrishiexAccount.objects.get(bank_name=str(request_data.get('acc_name')))
       
    '''Creating Transaction Object'''
    transaction_obj = Transaction.objects.create(payment_method=str(request_data.get('payment_type')),
                                                 transaction_no=str(request_data.get('transaction_no')),
                                                 bank_details=str(request_data.get('bank_details')),
                                                 channel_partner=channel_partner_obj,
                                                 krishiex_account=krichiex_acc_obj)
    '''Update Payment object and Order Status'''
    for itr in range(0,len(order_ids)):
        try:
            payment_obj = Payment.objects.get(delivery=Delivery.objects.get(order=Order.objects.get(sales_order_id=order_ids[itr])))
            payment_obj.transaction=transaction_obj
            payment_obj.save()
            order_obj = Order.objects.get(sales_order_id=order_ids[itr])
            order_obj.status=str(request_data.get('status'))
            order_obj.save()
        except ObjectDoesNotExist:
            return {"errorCode":"400",
                 "errorMessage":"Payment Not Recieved "}
    
    return "success"
    