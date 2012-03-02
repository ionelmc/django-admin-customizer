from django.db import models
from django.db.models import Q
from django.db.models.fields.related import RelatedField
from django.contrib.contenttypes.models import ContentType

from . import conf

def get_type_for(field):
    if isinstance(field, models.ForeignKey):
        return 'fk'
    elif isinstance(field, models.ManyToManyField):
        return 'mtm'
    elif isinstance(field, models.OneToOneField):
        return 'oto'
    else:
        return 'other'

def get_target_for(field):
    if isinstance(field, RelatedField):
        model = field.rel.to
        if issubclass(model, models.Model):
            return ContentType.objects.get_for_model(model)
        elif isinstance(model, ContentType):
            return model
        else:
            raise RuntimeError("Unknown model %s." % model)
    else:
        return None

class AvailableFieldManager(models.Manager):
    def get_by_field(self, model, field, through=None):
        return self.get(
            name = field.name,
            type = get_type_for(field),
            target = get_target_for(field),
            model = model
        )

    def create_by_field(self, model, field, through=None):
        return self.create(
            name = field.name,
            type = get_type_for(field),
            target = get_target_for(field),
            model = model
        )

    def get_or_create_by_field(self, model, field, through=None):
        try:
            return self.get_by_field(model, field, through), False
        except self.model.DoesNotExist:
            return self.create_by_field(model, field), True


    def filter_reachable_for_model(self, model):
        query = Q(model=model)
        for level in range(1, conf.ADMIN_CUSTOMIZER_MAX_FIELD_DEPTH + 1):
            query |= Q(**{'reachable_through__'*level + 'model': model})
        return self.filter(query)
