from DBLayer.order_management.models import Order

def handle_request(orderId,status):
    order_obj=Order.objects.get(sales_order_id=int(orderId))
    order_obj.status = str(status)
    order_obj.save()
    return "Success"