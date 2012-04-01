from django import forms
from django.contrib import admin
from django.contrib.admin.options import flatten_fieldsets
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from .models import AdminSite, AvailableField, RegisteredModel
from .widgets import FieldSelect
from .fields import FieldSelectField, ContentTypeChoiceField

admin.site.register(AdminSite)

def registered_model_form_factory(model):
    if model:
        class EditRegisteredModelForm(forms.ModelForm):
            class Meta:
                model = RegisteredModel

            list_display = FieldSelectField(
                _('"list_display" (changelist columns)'),
                model,
                AvailableField.objects.filter_for_model(model=model).filter(
                    type__in = AvailableField.LIST_DISPLAY_TYPES
                ),
            )
            list_filter = FieldSelectField(
                _('"list_filter" (changelist filters)'),
                model,
                AvailableField.objects.filter_reachable_for_model(model).filter(
                    type__in = AvailableField.LIST_FILTER_TYPES
                ),
            )
            search_fields = FieldSelectField(
                _('"search_fields" (changelist search)'),
                model,
                AvailableField.objects.filter_reachable_for_model(model).filter(
                    type__in = AvailableField.SEARCH_FIELDS_TYPES
                ),
            )
            raw_id_fields = FieldSelectField(
                _('"raw_id_fields" (id-editable in changelist/edit/add)'),
                model,
                AvailableField.objects.filter_for_model(
                    model,
                    type__in = AvailableField.RAW_ID_FIELDS_TYPES
                ),
            )
        return EditRegisteredModelForm
    else:
        class AddRegisteredModelForm(forms.ModelForm):
            class Meta:
                model = RegisteredModel

            model = ContentTypeChoiceField(ContentType.objects.order_by('app_label', 'model'))
        return AddRegisteredModelForm

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
        kwargs['form'] = registered_model_form_factory(obj and obj.model)
        return super(RegisteredModelAdmin, self).get_form(request, obj=obj, **kwargs)

admin.site.register(RegisteredModel, RegisteredModelAdmin)

class AvailableFieldAdmin(admin.ModelAdmin):
    list_display = 'name', 'model', 'type', 'target', 'through_display'

    def through_display(self, obj):
        return "AF:%s" % obj.through_id
    through_display.short_description = "Through"
    through_display.admin_order_field = "through"

admin.site.register(AvailableField, AvailableFieldAdmin)
