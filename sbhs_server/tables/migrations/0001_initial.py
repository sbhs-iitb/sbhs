# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Board'
        db.create_table(u'tables_board', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('mid', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('online', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'tables', ['Board'])

        # Adding model 'Account'
        db.create_table(u'tables_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('trashed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=127)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('board', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tables.Board'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'tables', ['Account'])

        # Adding model 'Slot'
        db.create_table(u'tables_slot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('start_hour', self.gf('django.db.models.fields.IntegerField')()),
            ('start_minute', self.gf('django.db.models.fields.IntegerField')()),
            ('end_hour', self.gf('django.db.models.fields.IntegerField')()),
            ('end_minute', self.gf('django.db.models.fields.IntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'tables', ['Slot'])

        # Adding model 'Booking'
        db.create_table(u'tables_booking', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tables.Account'])),
            ('slot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tables.Slot'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'tables', ['Booking'])

        # Adding model 'Experiment'
        db.create_table(u'tables_experiment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('booking', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tables.Booking'])),
            ('log', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'tables', ['Experiment'])


    def backwards(self, orm):
        # Deleting model 'Board'
        db.delete_table(u'tables_board')

        # Deleting model 'Account'
        db.delete_table(u'tables_account')

        # Deleting model 'Slot'
        db.delete_table(u'tables_slot')

        # Deleting model 'Booking'
        db.delete_table(u'tables_booking')

        # Deleting model 'Experiment'
        db.delete_table(u'tables_experiment')


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
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
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