#!/bin/bash

echo "Removing all pyc file"
find ../ -iname \*.pyc -exec rm -rfv {} \;

service apache2 restart
#service mysql restart
