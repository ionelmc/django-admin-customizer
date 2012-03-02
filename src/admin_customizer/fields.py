from django.forms.models import ModelMultipleChoiceField, ModelChoiceIterator, ChoiceField
from .widgets import FieldSelect

class FieldSelectChoice(object):
    # we use this instead of collections.namedtuple because django typechecks
    # the options (list/tuples are option groups)
    def __init__(self, verbose_label, label, parent):
        self.verbose_label, self.label, self.parent = verbose_label, label, parent

class FieldSelectChoiceIterator(ModelChoiceIterator):
    def choice(self, obj):
        return (self.field.prepare_value(obj), FieldSelectChoice(self.field.label_from_instance(obj), obj.name, self.field.prepare_value(obj.through)))

class FieldSelectField(ModelMultipleChoiceField):

    def __init__(self, verbose_name, queryset, **kwargs):
        self.widget = FieldSelect(verbose_name)
        super(FieldSelectField, self).__init__(queryset, **kwargs)

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return FieldSelectChoiceIterator(self)
    choices = property(_get_choices, ChoiceField._set_choices)
