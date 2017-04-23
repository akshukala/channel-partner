from datetime import datetime
import os
from os.path import dirname
from flask_restful import Resource
from flask import current_app as app
from flask.helpers import send_from_directory

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code39, code128, code93
from reportlab.lib.pagesizes import A4, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Frame, Spacer
from flask import request

from DBLayer.inventory.models import Delivery
from DBLayer.order_management.models import Order, OrderItem
from DBLayer.cpd.models import Channel_Partner
#from cpdservice.utils.auth import get_user

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
            os.makedirs(dir)

def create_pdf(path,user_id):
    
    current_user = Channel_Partner.objects.get(executive_id=int(user_id)).name
    delivery_obj = Delivery.objects.filter(order__status="RECIEVED AT CP",to_channel_partner=str(current_user))

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7.5
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 7.5
    styleBH.splitLongWords=1
    
    style_main = ParagraphStyle(name='Header',
            alignment=TA_CENTER,
            fontSize=9.5,)
    
    style_header = ParagraphStyle(name='Header',
            alignment=TA_LEFT,
            fontSize=8,)
    data=[]
    data_header=[]
    elements = []
    doc = SimpleDocTemplate(path, pagesize=A4)
    
    # file header
    header_para_title = Paragraph("<b>Recieved Order List</b>",style=style_main)
    header_para = Paragraph('''<b>KrishiEx</b><br/>
                               <b>Date: ''' + str(datetime.today().strftime("%d/%m/%y")) + '''</b>''',style=style_header)
    elements.append(header_para_title)
    elements.append(header_para)
    # Headers
    data_header.append(Paragraph('''<b>Sr. No</b>''', styleBH))
    data_header.append(Paragraph('''<b>Order No</b>''', styleBH))
    data_header.append(Paragraph('''<b>Name</b>''', styleBH))
    data_header.append(Paragraph('''<b>Mobile No</b>''', styleBH))
    data_header.append(Paragraph('''<b>Order Date</b>''', styleBH))
    data_header.append(Paragraph('''<b>Items</b>''', styleBH))
    data_header.append(Paragraph('''<b>Qty</b>''', styleBH))
    data_header.append(Paragraph('''<b>Address</b>''', styleBH))
    data_header.append(Paragraph('''<b>Amount</b>''', styleBH))
    data.append(data_header)
    
    # Texts
#     cod_sum=0
#     wt_sum =0
    for i,delivery in enumerate(delivery_obj):
        order_data=[]
#         barcode_list=[]
    
        farmer_address_1 =  (str(delivery.order.billing_address.street).title()) + " " +\
                             str(delivery.order.billing_address.village) + " - " + \
                             str(delivery.order.billing_address.post_office) + " - " +\
                             str(delivery.order.billing_address.taluka) + " - " +\
                             str(delivery.order.billing_address.district) + "-"+\
                             str(delivery.order.billing_address.pin_code)
        order_items = OrderItem.objects.filter(order=delivery.order)
        orderitem_list =""
        orderitem_qty =""
        for j,oi in enumerate(order_items):
            orderitem = oi.item_name.split('-')
#             orderItemList.append(orderitem[1])
#             order_qty_list.append(oi.quantity)
            if j == (len(order_items)-1):
                orderitem_list += str(orderitem[1])
                orderitem_qty += str(oi.quantity)
            else:
                orderitem_list += str(orderitem[1]) + ", "
                orderitem_qty += str(oi.quantity) + ", "
#         farmer_address_2 = str(order.billing_address.district) 
#         delivery_obj = Delivery.objects.get(order=order)
#         cod_sum = cod_sum + int(order.cod_amount)
#         wt_sum = wt_sum + int(delivery_obj.total_weight)
#         barcode = code128.Code128(str(delivery_obj.indiaPost_barcode_no))
#         barcode_list.append(barcode)
#         barcode_list.append(Paragraph(str(delivery_obj.indiaPost_barcode_no), styleN))
        order_data.append(Paragraph(str(i+1), styleN))
        order_data.append(Paragraph(str(delivery.order.sales_order_id), styleN))
        order_data.append(Paragraph(str((delivery.order.owner.first_name).title()) + " " + str((delivery.order.owner.middle_name).title()) + " " 
                                    + str((delivery.order.owner.last_name).title()), styleN))
        order_data.append(Paragraph(str(delivery.order.notification_mobile), styleN))
        order_data.append(Paragraph((delivery.order.created_on).strftime('%d/%m/%y'), styleN))
        order_data.append(Paragraph(orderitem_list, styleN))
        order_data.append(Paragraph(orderitem_qty, styleN))
        order_data.append(Paragraph(farmer_address_1, styleN))
        order_data.append(Paragraph(str(int(delivery.order.cod_amount)), styleN))
#         order_data.append(barcode_list)
        data.append(order_data)
    
    table = Table(data, colWidths=[0.5 * cm, 1.0 * cm, 2.2 * cm,
                                   2.0* cm, 1.2 * cm, 2.0 * cm, 0.7 * cm, 3.2 * cm, 1.0 * cm], repeatRows=1)
    
    table.setStyle(TableStyle([
                           ('ALIGN',(0,0),(-1,-1),'CENTER'),
                           ('LEFTPADDING', (0,0), (-1,-1), 3),
                           ('RIGHTPADDING', (0,0), (-1,-1), 1),
                           ('FONTSIZE', (0,0), (-1,1), 5),
                           ('FONTSIZE', (0, 4), (-1, 4), 5),
                           ('FONTNAME', (0,0), (-1,0), 'Times-Bold'), 
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ]))
#     footer_para = Paragraph('''<b>Total Weight: ''' + str(wt_sum) + '''gms</b><br/>
#                               <b>Total Amount: Rs.''' + str(cod_sum) + '''</b>''',style=style_main)
    
    elements.append(table)
#     elements.append(footer_para)
    doc.build(elements)
    
class RecievedOrderList(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        UPLOAD_FOLDER = os.path.join(dirname(app.root_dir), 'Documents')
        filename = str(datetime.today().strftime("%d_%m_%y")) + "Recieved_order_list.pdf" 
        path = os.path.join(UPLOAD_FOLDER,filename)
        assure_path_exists(path)
        create_pdf(path,user_id)
        return send_from_directory(directory=UPLOAD_FOLDER,filename=filename)