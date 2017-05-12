#!/bin/bash

find /home/vlabs/sbhs_vlabs/sbhs/ -iname \*.pyc -exec rm -rfv {} \; #to delete all .pyc files

DIR="$( cd "$( dirname "$0" )" && pwd )"
cd $DIR
killall streamer
source ../bin/activate
#source ./bin/activate
python sbhs_server/scan_machines.py
#python offline_reconnect.py
python manage.py syncdb
python manage.py migrate tables
python manage.py migrate slot
python manage.py initialize_machines
python manage.py generate_checksum
touch index.wsgi
python log_generator.py
date > date.txt
sleep 2
#python sbhs_server/load_homepage.py #commented by srikant
