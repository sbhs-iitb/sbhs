# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Experiment.checksum'
        db.delete_column(u'tables_experiment', 'checksum')


    def backwards(self, orm):
        # Adding field 'Experiment.checksum'
        db.add_column(u'tables_experiment', 'checksum',
                      self.gf('django.db.models.fields.CharField')(default='0', max_length=127),
                      keep_default=False)


    models = {
        u'tables.account': {
            'Meta': {'object_name': 'Account'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tables.Board']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'trashed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '127'})
        },
        u'tables.board': {
            'Meta': {'object_name': 'Board'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'online': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'trashed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'tables.booking': {
            'Meta': {'object_name': 'Booking'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tables.Account']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tables.Slot']"}),
            'trashed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'tables.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'booking': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tables.Booking']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'trashed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'tables.slot': {
            'Meta': {'object_name': 'Slot'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_hour': ('django.db.models.fields.IntegerField', [], {}),
            'end_minute': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_hour': ('django.db.models.fields.IntegerField', [], {}),
            'start_minute': ('django.db.models.fields.IntegerField', [], {}),
            'trashed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['tables']