from DBLayer.settings.pool import init_pool
from os.path import dirname, abspath

import django
from django.db import close_old_connections
from flask import Flask
from flask.ext import restful


from cpdservice.conf.config_logger_setup import setup_config_logger
from cpdservice.session.interfaces import DBInterface
from flask.ext.cors import CORS
from cpdservice.service_apis.ping import Ping
from cpdservice.service_apis.Channel_partner_delivery import Channel_partner_delivery
from cpdservice.service_apis.Manage_orders import Manage_Orders
from cpdservice.service_apis.Manage_Payments import Manage_Payments
from cpdservice.service_apis.Reports import Reports
from cpdservice.service_apis.Recieved_orders_to_pdf import RecievedOrderList
from cpdservice.service_apis.Channel_partner_summary import Channel_partner_summary

close_old_connections()
init_pool()

django.setup()
app = Flask(__name__)
CORS(app)
app.auth_header_name = 'X-Authorization-Token'
app.session_interface = DBInterface()
app.root_dir = dirname(dirname(abspath(__file__)))

api = restful.Api(app)

setup_config_logger(app)

app.logger.info("Setting up Resources")
api.add_resource(Ping,'/cpdservice/ping/')
api.add_resource(Channel_partner_delivery,'/cpdservice/incoming_package/')
api.add_resource(Manage_Orders,'/cpdservice/managing_package/')
api.add_resource(Manage_Payments,'/cpdservice/managing_payments/')
api.add_resource(Reports,'/cpdservice/manage_reports/')
api.add_resource(RecievedOrderList,'/cpdservice/recieved_list/')
api.add_resource(Channel_partner_summary,'/cpdservice/summary/')
app.logger.info("Resource setup done")

if __name__ == '__main__':
    # from gevent import monkey
    # from crmadminservice.utils.hacks import gevent_django_db_hack
    # gevent_django_db_hack()
    # monkey.patch_all(socket=True, dns=True, time=True, select=True, thread=False, os=True, ssl=True, httplib=False, aggressive=True)
    app.run(host="0.0.0.0", port=9856,threaded=True)
