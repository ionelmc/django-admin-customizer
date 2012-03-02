from django import forms
from django.contrib import admin
from django.contrib.admin.options import flatten_fieldsets
from django.utils.translation import ugettext_lazy as _

from .models import AdminSite, AvailableField, RegisteredModel
from .widgets import FieldSelect
from .fields import FieldSelectField

admin.site.register((AdminSite, AvailableField))

def registered_model_form_factory(model):
    class RegisteredModelForm(forms.ModelForm):
        class Meta:
            model = RegisteredModel

        list_display = FieldSelectField(
            _('Fields for "list_display" (changelist columns)'),
            AvailableField.objects.filter(model=model),
        )
        list_filter = FieldSelectField(
            _('Fields for "list_filter" (changelist filters)'),
            AvailableField.objects.filter_reachable_for_model(model),
        )
        search_fields = FieldSelectField(
            _('Fields for "search_fields" (changelist search)'),
            AvailableField.objects.filter_reachable_for_model(model),
        )
        raw_id_fields = FieldSelectField(
            _('Fields for "raw_id_fields" (id-editable in changelist/edit/add)'),
            AvailableField.objects.filter(model=model, type__in=('fk', 'mtm')),
        )
    return RegisteredModelForm

class RegisteredModelAdmin(admin.ModelAdmin):
    def get_fieldsets(self, request, obj=None):
        if obj:
            return (
                (_('Summary'), {
                    'fields': ('model', 'admin_site')

                }),
                (_('Changelist settings'), {
                    'fields': ('list_display', 'list_filter', 'search_fields')
                }),
                (_('Other settings'), {
                    'fields': ('raw_id_fields',)
                })
            )
        else:
            return (
                (_('Summary'), {
                    'fields': ('model', 'admin_site')
                }),
            )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return 'model',
        else:
            return set(flatten_fieldsets(self.get_fieldsets(request, obj))) - set(('model', 'admin_site'))

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            kwargs['form'] = registered_model_form_factory(obj.model)
        return super(RegisteredModelAdmin, self).get_form(request, obj=obj, **kwargs)

admin.site.register(RegisteredModel, RegisteredModelAdmin)
