import csv
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from DBLayer.inventory.models import Delivery
from DBLayer.order_management.models import OrderStatusHistory
from DBLayer.cpd.models import Incentive,Channel_Partner,Transaction,KrishiexAccount,Payment


def create_order_csv(file_path,from_date,to_date,user_id):
    f_date = datetime.strptime(str(from_date), "%Y-%m-%d %H:%M:%S")
    t_date = datetime.strptime(str(to_date), "%Y-%m-%d %H:%M:%S")
    channel_partner_name = Channel_Partner.objects.get(executive=User.objects.get(id=int(user_id))).name
    delivery_objs = Delivery.objects.filter(to_channel_partner=str(channel_partner_name),order__created_on__gte=f_date, order__created_on__lte= t_date)
    response = []
    for delivery in delivery_objs:
        order_list = []
        order_list.append(delivery.order.sales_order_id)
        order_list.append(delivery.order.owner.first_name.title() +" "+ delivery.order.owner.middle_name.title()
                          + " " + delivery.order.owner.last_name)
        order_list.append(delivery.order.created_on.strftime("%d-%m-%y"))
        try:
            recieved_date_exists = OrderStatusHistory.objects.get(status='RECIEVED AT CP',order=delivery.order).created_on.strftime("%d-%m-%Y")
            order_list.append(recieved_date_exists)
        except ObjectDoesNotExist:
            order_list.append("-")
        try:
            delivered_date_exists = OrderStatusHistory.objects.get(status='DELIVERED BY CP',order=delivery.order).created_on.strftime("%d-%m-%Y")
            order_list.append(delivered_date_exists)
        except ObjectDoesNotExist:
            order_list.append("-")
        try:
            payment_date_exists = OrderStatusHistory.objects.get(status='PAYMENT BY CP',order=delivery.order).created_on.strftime("%d-%m-%Y")
            order_list.append(payment_date_exists)
        except ObjectDoesNotExist:
            order_list.append("-")
        try:
            complete_date_exists = OrderStatusHistory.objects.get(status='ORDER COMPLETED',order=delivery.order).created_on.strftime("%d-%m-%Y")
            order_list.append(complete_date_exists)
        except ObjectDoesNotExist:
            order_list.append("-")
        order_list.append(delivery.order.status) 
        order_list.append(delivery.order.grand_total)
        order_list.append(delivery.total_weight)
        try:
            order_list.append(Incentive.objects.get(delivery=delivery).incentive)    
        except ObjectDoesNotExist:
            order_list.append("-")
        response.append(order_list)
    header = ["Order Id", "Customer Name","Order Date" ,"Recieved Date","Delivery Date" ,
              "Payment Deposit Date","Order Completion Date","Status","Amount","Weight","Incentive Earned"]

    with open(file_path, 'wb') as output_file:
        head_writer = csv.writer(output_file,delimiter=',')
        head_writer.writerow(['Order Report'])
        head_writer.writerow(["Report Generation Date", str(datetime.today().strftime("%d-%m-%y"))])
        head_writer.writerow(header)
        for order in response:
            head_writer.writerow(order)


def create_transaction_csv(file_path,from_date,to_date,user_id):
    f_date = datetime.strptime(str(from_date), "%Y-%m-%d %H:%M:%S")
    t_date = datetime.strptime(str(to_date), "%Y-%m-%d %H:%M:%S")
    channel_partner = Channel_Partner.objects.get(executive=User.objects.get(id=int(user_id)))
    transaction_objs = Transaction.objects.filter(channel_partner=channel_partner, created_on__gte=f_date, created_on__lte= t_date)
    response = []
    for transaction_obj in transaction_objs:
        transaction_list = []
        transaction_list.append((transaction_obj.created_on).strftime("%d-%m-%y"))
        transaction_list.append(transaction_obj.transaction_no)
        transaction_list.append(KrishiexAccount.objects.get(account_no=transaction_obj.krishiex_account.account_no).bank_name)
        transaction_list.append(Payment.objects.filter(transaction=transaction_obj.id).count())
        transaction_list.append(transaction_obj.status)
        response.append(transaction_list)
    header = ["Deposit Date", "Transaction Id", "Transfered to Account", "Total Packages", 
              "Transaction Status"]
    with open(file_path, 'wb') as output_file:
        head_writer = csv.writer(output_file, delimiter=',')
        head_writer.writerow(['Transaction Report'])
        head_writer.writerow(["Report Generation Date", str(datetime.today().strftime("%d-%m-%y"))])
        head_writer.writerow(header)
        for transaction in response:
            head_writer.writerow(transaction) 