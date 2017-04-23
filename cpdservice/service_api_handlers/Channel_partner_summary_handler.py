from django.contrib.auth.models import User
from django.db.models import Count
from cpdservice.utils.auth import get_user
from DBLayer.inventory.models import Delivery
from DBLayer.cpd.models import Channel_Partner

def handle_request():
	response=[]
	user_id = get_user().id
	
	channel_partner_name = Channel_Partner.objects.get(executive=User.objects.get(id=user_id)).name
	incoming_packages_count = len(Delivery.objects.filter(to_channel_partner=str(channel_partner_name),order__status='DISPATCHED'))
			
	delivered_packages_count = len(Delivery.objects.filter(to_channel_partner=str(channel_partner_name),order__status='DELIVERED BY CP'))
			
	pending_packages_count = len(Delivery.objects.filter(to_channel_partner=str(channel_partner_name),order__status='RECIEVED AT CP'))
			
	pending_more_packages_count = len(Delivery.objects.filter(to_channel_partner=str(channel_partner_name),order__status='RECIEVED AT CP'))
			
	returned_packages_count = len(Delivery.objects.filter(to_channel_partner=str(channel_partner_name),order__status='RETURNED TO CP'))
			

	response.append({'incoming_packages_count':incoming_packages_count})
	response.append({'delivered_packages_count':delivered_packages_count})
	response.append({'pending_packages_count':pending_packages_count})
	response.append({'pending_more_packages_count':pending_more_packages_count})
	response.append({'returned_packages_count':returned_packages_count})

	return response