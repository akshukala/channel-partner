
sudo rm /etc/nginx/sites-enabled/default
sudo cp $PYTHONPATH/crmservice/conf/crmservice_nginx.conf /etc/nginx/sites-enabled/
pkill gunicorn
cd $PYTHONPATH/crmservice/conf
echo $PWD
gunicorn -c gunicorn.py service_app:app
sudo service nginx restart
