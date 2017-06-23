#!/bin/bash

# Django 1.11 compatible


find $(pwd) -iname \*.pyc -exec rm -rfv {} \; #to delete all .pyc files

DIR="$( cd "$( dirname "$0" )" && pwd )"
cd $DIR
killall streamer
rm production_static_files/img/webcam/*.jpeg
source ../venv/bin/activate
#source ./bin/activate
python sbhs_server/scan_machines.py
#python offline_reconnect.py
python manage.py makemigrations
python manage.py migrate
python manage.py initialize_machines
python manage.py generate_checksum
touch index.wsgi
python manage.py log_generator

#python log_generator.py
date > date.txt
sleep 2
