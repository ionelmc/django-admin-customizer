from django.db import models
from django.db.models import Q
from django.db.models.fields.related import RelatedField
from django.contrib.contenttypes.models import ContentType

from . import conf


class AvailableFieldManager(models.Manager):
    def filter_reachable_for_model(self, model):
        query = Q(model=model, through__isnull=True)
        for level in range(1, conf.ADMIN_CUSTOMIZER_MAX_FIELD_DEPTH + 1):
            query |= Q(**{'through__'*level + 'model': model, 'through__'*level + 'through__isnull': True})
        return self.filter(query)

    def filter_for_model(self, model, **extra):
        return self.filter(model=model, through__isnull=True, **extra)
