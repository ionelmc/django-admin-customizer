# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AdminSite'
        db.create_table('admin_customizer_adminsite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('admin_customizer', ['AdminSite'])

        # Adding model 'RegisteredModel'
        db.create_table('admin_customizer_registeredmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('admin_customizer', ['RegisteredModel'])

        # Adding M2M table for field list_display on 'RegisteredModel'
        db.create_table('admin_customizer_registeredmodel_list_display', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('registeredmodel', models.ForeignKey(orm['admin_customizer.registeredmodel'], null=False)),
            ('availablefield', models.ForeignKey(orm['admin_customizer.availablefield'], null=False))
        ))
        db.create_unique('admin_customizer_registeredmodel_list_display', ['registeredmodel_id', 'availablefield_id'])

        # Adding M2M table for field list_filter on 'RegisteredModel'
        db.create_table('admin_customizer_registeredmodel_list_filter', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('registeredmodel', models.ForeignKey(orm['admin_customizer.registeredmodel'], null=False)),
            ('availablefield', models.ForeignKey(orm['admin_customizer.availablefield'], null=False))
        ))
        db.create_unique('admin_customizer_registeredmodel_list_filter', ['registeredmodel_id', 'availablefield_id'])

        # Adding M2M table for field search_fields on 'RegisteredModel'
        db.create_table('admin_customizer_registeredmodel_search_fields', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('registeredmodel', models.ForeignKey(orm['admin_customizer.registeredmodel'], null=False)),
            ('availablefield', models.ForeignKey(orm['admin_customizer.availablefield'], null=False))
        ))
        db.create_unique('admin_customizer_registeredmodel_search_fields', ['registeredmodel_id', 'availablefield_id'])

        # Adding M2M table for field raw_id_fields on 'RegisteredModel'
        db.create_table('admin_customizer_registeredmodel_raw_id_fields', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('registeredmodel', models.ForeignKey(orm['admin_customizer.registeredmodel'], null=False)),
            ('availablefield', models.ForeignKey(orm['admin_customizer.availablefield'], null=False))
        ))
        db.create_unique('admin_customizer_registeredmodel_raw_id_fields', ['registeredmodel_id', 'availablefield_id'])

        # Adding model 'AvailableField'
        db.create_table('admin_customizer_availablefield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['contenttypes.ContentType'])),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['contenttypes.ContentType'])),
            ('through', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['admin_customizer.AvailableField'], null=True, blank=True)),
        ))
        db.send_create_signal('admin_customizer', ['AvailableField'])


    def backwards(self, orm):
        
        # Deleting model 'AdminSite'
        db.delete_table('admin_customizer_adminsite')

        # Deleting model 'RegisteredModel'
        db.delete_table('admin_customizer_registeredmodel')

        # Removing M2M table for field list_display on 'RegisteredModel'
        db.delete_table('admin_customizer_registeredmodel_list_display')

        # Removing M2M table for field list_filter on 'RegisteredModel'
        db.delete_table('admin_customizer_registeredmodel_list_filter')

        # Removing M2M table for field search_fields on 'RegisteredModel'
        db.delete_table('admin_customizer_registeredmodel_search_fields')

        # Removing M2M table for field raw_id_fields on 'RegisteredModel'
        db.delete_table('admin_customizer_registeredmodel_raw_id_fields')

        # Deleting model 'AvailableField'
        db.delete_table('admin_customizer_availablefield')


    models = {
        'admin_customizer.adminsite': {
            'Meta': {'object_name': 'AdminSite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'admin_customizer.availablefield': {
            'Meta': {'object_name': 'AvailableField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'through': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin_customizer.AvailableField']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'admin_customizer.registeredmodel': {
            'Meta': {'object_name': 'RegisteredModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_display': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'registeredmodels_with_list_display'", 'symmetrical': 'False', 'to': "orm['admin_customizer.AvailableField']"}),
            'list_filter': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'registeredmodels_with_list_filter'", 'symmetrical': 'False', 'to': "orm['admin_customizer.AvailableField']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'raw_id_fields': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'registeredmodels_with_'", 'symmetrical': 'False', 'to': "orm['admin_customizer.AvailableField']"}),
            'search_fields': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'registeredmodels_with_search_fields'", 'symmetrical': 'False', 'to': "orm['admin_customizer.AvailableField']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['admin_customizer']
