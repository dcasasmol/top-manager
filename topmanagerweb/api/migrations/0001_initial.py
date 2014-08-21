# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table(u'api_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('flag', self.gf('django.db.models.fields.files.ImageField')(default='flags/default-flag.png', max_length=100)),
            ('tm_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'api', ['Country'])

        # Adding model 'Position'
        db.create_table(u'api_position', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('img', self.gf('django.db.models.fields.files.ImageField')(default='positions/default-position.png', max_length=100)),
            ('pitch_img', self.gf('django.db.models.fields.files.ImageField')(default='positions/base-pitch.png', max_length=100)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'api', ['Position'])

        # Adding model 'League'
        db.create_table(u'api_league', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='leagues', to=orm['api.Country'])),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(default='leagues/default-logo.jpg', max_length=100)),
            ('tm_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('tm_slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
        ))
        db.send_create_signal(u'api', ['League'])

        # Adding model 'Club'
        db.create_table(u'api_club', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('crest', self.gf('django.db.models.fields.files.ImageField')(default='clubs/default-crest.jpg', max_length=100)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='clubs', to=orm['api.Country'])),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(related_name='leagues', to=orm['api.League'])),
            ('stadium', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('seats', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True, blank=True)),
            ('tm_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('tm_slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
        ))
        db.send_create_signal(u'api', ['Club'])

        # Adding model 'Injury'
        db.create_table(u'api_injury', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('duration', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'api', ['Injury'])

        # Adding model 'Footballer'
        db.create_table(u'api_footballer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('arrived_date', self.gf('django.db.models.fields.DateField')(default=None, null=True, blank=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(default=None, null=True, blank=True)),
            ('birth_place', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(default='footballers/default-photo.jpg', max_length=100)),
            ('captain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='footballers', null=True, to=orm['api.Club'])),
            ('contract_until', self.gf('django.db.models.fields.DateField')(default=None, null=True, blank=True)),
            ('foot', self.gf('django.db.models.fields.CharField')(default=None, max_length=255)),
            ('full_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('height', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
            ('injury', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='footballer', unique=True, null=True, to=orm['api.Injury'])),
            ('new_arrival_from', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sales', null=True, to=orm['api.Club'])),
            ('new_arrival_price', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('tm_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('tm_slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'api', ['Footballer'])

        # Adding model 'Nationality'
        db.create_table(u'api_nationality', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nationalizated', to=orm['api.Country'])),
            ('footballer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nationalizated', to=orm['api.Footballer'])),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'api', ['Nationality'])

        # Adding model 'PlayingPosition'
        db.create_table(u'api_playingposition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('footballer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='playing', to=orm['api.Footballer'])),
            ('position', self.gf('django.db.models.fields.related.ForeignKey')(related_name='playing', to=orm['api.Position'])),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'api', ['PlayingPosition'])


    def backwards(self, orm):
        # Deleting model 'Country'
        db.delete_table(u'api_country')

        # Deleting model 'Position'
        db.delete_table(u'api_position')

        # Deleting model 'League'
        db.delete_table(u'api_league')

        # Deleting model 'Club'
        db.delete_table(u'api_club')

        # Deleting model 'Injury'
        db.delete_table(u'api_injury')

        # Deleting model 'Footballer'
        db.delete_table(u'api_footballer')

        # Deleting model 'Nationality'
        db.delete_table(u'api_nationality')

        # Deleting model 'PlayingPosition'
        db.delete_table(u'api_playingposition')


    models = {
        u'api.club': {
            'Meta': {'ordering': "['name']", 'object_name': 'Club'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clubs'", 'to': u"orm['api.Country']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'crest': ('django.db.models.fields.files.ImageField', [], {'default': "'clubs/default-crest.jpg'", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'leagues'", 'to': u"orm['api.League']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'seats': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'stadium': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'tm_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'tm_slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'api.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.files.ImageField', [], {'default': "'flags/default-flag.png'", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tm_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'api.footballer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Footballer'},
            'arrived_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'birth_place': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'captain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'footballers'", 'null': 'True', 'to': u"orm['api.Club']"}),
            'contract_until': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'foot': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255'}),
            'full_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'height': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'injury': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'footballer'", 'unique': 'True', 'null': 'True', 'to': u"orm['api.Injury']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nationalities': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'footballers'", 'symmetrical': 'False', 'through': u"orm['api.Nationality']", 'to': u"orm['api.Country']"}),
            'new_arrival_from': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sales'", 'null': 'True', 'to': u"orm['api.Club']"}),
            'new_arrival_price': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'default': "'footballers/default-photo.jpg'", 'max_length': '100'}),
            'positions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'footballers'", 'symmetrical': 'False', 'through': u"orm['api.PlayingPosition']", 'to': u"orm['api.Position']"}),
            'tm_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'tm_slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'api.injury': {
            'Meta': {'ordering': "['name']", 'object_name': 'Injury'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'duration': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'api.league': {
            'Meta': {'ordering': "['name']", 'object_name': 'League'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'leagues'", 'to': u"orm['api.Country']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'default': "'leagues/default-logo.jpg'", 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tm_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'tm_slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'api.nationality': {
            'Meta': {'ordering': "['name']", 'object_name': 'Nationality'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nationalizated'", 'to': u"orm['api.Country']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'footballer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nationalizated'", 'to': u"orm['api.Footballer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'api.playingposition': {
            'Meta': {'ordering': "['name']", 'object_name': 'PlayingPosition'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'footballer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'playing'", 'to': u"orm['api.Footballer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'playing'", 'to': u"orm['api.Position']"}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'api.position': {
            'Meta': {'ordering': "['name']", 'object_name': 'Position'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'default': "'positions/default-position.png'", 'max_length': '100'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pitch_img': ('django.db.models.fields.files.ImageField', [], {'default': "'positions/base-pitch.png'", 'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['api']
