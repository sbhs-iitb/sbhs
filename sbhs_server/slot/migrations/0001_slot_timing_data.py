# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from sbhs_server.tables.models import Slot

class Migration(DataMigration):

    def forwards(self, orm):
        # "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        for i in xrange(24):
            Slot.objects.create(start_hour=i, end_hour=i, start_minute=0, end_minute=55) 

    def backwards(self, orm):
        # "Write your backwards methods here."
        for i in xrange(24):
            Slot.objects.delete(i)
        

    models = {
        
    }

    complete_apps = ['slot']
    symmetrical = True
