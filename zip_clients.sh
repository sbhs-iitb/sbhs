#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"
cd $DIR
#source ../bin/activate
source bin/activate

cd client_static/scilab_codes/
find -iname run | xargs rm
find -iname run.vbs | xargs rm
find -iname *~ | xargs rm
find -iname sbhsclient* | xargs rm
find -iname 20*.txt | xargs rm
find -iname settings.txt | xargs rm
find -iname clientread.sce | xargs rm
find -iname clientwrite.sce | xargs rm
cd ../../
python manage.py zip_client
python manage.py collectstatic
