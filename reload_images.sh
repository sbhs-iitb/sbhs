#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"
cd $DIR
source ../bin/activate
python manage.py reload_images