# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'RegisteredModel.admin_site'
        db.add_column('admin_customizer_registeredmodel', 'admin_site', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['admin_customizer.AdminSite']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'RegisteredModel.admin_site'
        db.delete_column('admin_customizer_registeredmodel', 'admin_site_id')


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
            'admin_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin_customizer.AdminSite']"}),
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
