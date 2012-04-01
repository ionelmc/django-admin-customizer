# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'RegisteredModel.created'
        db.add_column('admin_customizer_registeredmodel', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 4, 1, 16, 52, 39, 980149), blank=True), keep_default=False)

        # Adding field 'RegisteredModel.modified'
        db.add_column('admin_customizer_registeredmodel', 'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 4, 1, 16, 52, 48, 548422), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'RegisteredModel.created'
        db.delete_column('admin_customizer_registeredmodel', 'created')

        # Deleting field 'RegisteredModel.modified'
        db.delete_column('admin_customizer_registeredmodel', 'modified')


    models = {
        'admin_customizer.adminsite': {
            'Meta': {'object_name': 'AdminSite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'admin_customizer.availablefield': {
            'Meta': {'unique_together': "(('model', 'name', 'type', 'target', 'through'),)", 'object_name': 'AvailableField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'through': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin_customizer.AvailableField']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'admin_customizer.registeredmodel': {
            'Meta': {'unique_together': "(('model', 'admin_site'),)", 'object_name': 'RegisteredModel'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'admin_site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'models'", 'to': "orm['admin_customizer.AdminSite']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_display': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'registeredmodels_with_list_display'", 'blank': 'True', 'to': "orm['admin_customizer.AvailableField']"}),
            'list_filter': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'registeredmodels_with_list_filter'", 'blank': 'True', 'to': "orm['admin_customizer.AvailableField']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'raw_id_fields': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'+'", 'blank': 'True', 'to': "orm['admin_customizer.AvailableField']"}),
            'search_fields': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'registeredmodels_with_search_fields'", 'blank': 'True', 'to': "orm['admin_customizer.AvailableField']"})
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
