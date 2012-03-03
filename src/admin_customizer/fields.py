from django.forms.models import ModelMultipleChoiceField, ModelChoiceIterator
from django.forms.models import ChoiceField, ModelChoiceField

from .widgets import FieldSelect
from . import conf

class ContentTypeChoiceField(ModelChoiceField):
    def label_from_instance(self, cc):
        return "%s.%s" % (cc.app_label, cc.model)

class FieldSelectChoice(object):
    # we use this instead of collections.namedtuple because django typechecks
    # the options (list/tuples are option groups)
    def __init__(self, verbose_label, label, parent):
        self.verbose_label, self.label, self.parent = verbose_label, label, parent

class FieldSelectChoiceIterator(ModelChoiceIterator):
    def choice(self, obj):
        return (self.field.prepare_value(obj), FieldSelectChoice(self.field.label_from_instance(obj), obj.name, self.field.prepare_value(obj.through)))

class FieldSelectField(ModelMultipleChoiceField):

    def __init__(self, verbose_name, relative_to, queryset, **kwargs):
        self.widget = FieldSelect(verbose_name)
        self.relative_to = relative_to
        super(FieldSelectField, self).__init__(queryset, **kwargs)

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return FieldSelectChoiceIterator(self)
    choices = property(_get_choices, ChoiceField._set_choices)

    def label_from_instance(self, af):
        if not af.through:
            return af.name
        else:
            label = [af.name]
            level = 0
            while af.through and level < conf.ADMIN_CUSTOMIZER_MAX_FIELD_DEPTH:
                level += 1
                af = af.through
                label.append(af.name)

            label = '__'.join(reversed(label))
            if af.model != self.relative_to:
                return u"!!! %s.%s -- %s" % (
                    af.model,
                    label,
                    af
                )
            else:
                return label
