from logging import getLogger
logger = getLogger(__name__)

import sys

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import class_prepared
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.management import update_contenttypes
from django.db.models import get_apps, get_models, signals
from django.utils.encoding import smart_unicode
from django.utils.importlib import import_module

from .managers import AvailableFieldManager
from . import conf

class AdminSite(models.Model):
    slug = models.SlugField()
    def __unicode__(self):
        return u"admin:%s" % self.slug


class RegisteredModel(models.Model):
    class Meta:
        unique_together = 'model', 'admin_site'

    model = models.ForeignKey("contenttypes.ContentType")
    admin_site = models.ForeignKey("AdminSite", related_name="models")
    list_display = models.ManyToManyField(
        "AvailableField",
        related_name = "registeredmodels_with_list_display",
        blank = True,
    )
    list_filter = models.ManyToManyField(
        "AvailableField",
        related_name = "registeredmodels_with_list_filter",
        blank = True,
    )
    search_fields = models.ManyToManyField(
        "AvailableField",
        related_name = "registeredmodels_with_search_fields",
        blank = True,
    )
    raw_id_fields = models.ManyToManyField("AvailableField",
        related_name = "+",
        limit_choices_to = {'type__in': ('oto', 'fk', 'mtm')},
        blank = True,
    )

    def __unicode__(self):
        if self.model:
            return u"RegisteredModel: %s.%s" % (self.model.app_label, self.model.model)
        else:
            return u"RegisteredModel: blank"

class AvailableField(models.Model):
    class Meta:
        unique_together = 'model', 'name', 'type', 'target', 'through'

    model = models.ForeignKey("contenttypes.ContentType", related_name="+")
    name = models.TextField()
    LIST_DISPLAY_TYPES = ('fk', 'mtm', 'oto', 'rev', 'meth', 'other')
    LIST_FILTER_TYPES = ('fk', 'mtm', 'oto', 'rev', 'other')
    RAW_ID_FIELDS_TYPES = ('fk', 'mtm')
    SEARCH_FIELDS_TYPES = ('fk', 'mtm', 'oto', 'rev', 'other')
    TYPES = (
        ('fk', _("Foreign key field")),
        ('mtm', _("Many to many field")),
        ('oto', _("One to one field")),
        ('rev', _("One to many (reverse foreign key) field")),
        ('meth', _("Model method")),
        #('span', _("Field from related model"))
        ('other', _("Other type of field"))
    )
    type = models.CharField(max_length=10, choices=TYPES)
    target = models.ForeignKey(
        "contenttypes.ContentType",
        null = True,
        blank = True,
        related_name = "+"
    )
    through = models.ForeignKey("self", null=True, blank=True)

    objects = AvailableFieldManager()

    def __unicode__(self):
        return u"AvailableField #%s %s.%s (%s)%s" % (
            self.id,
            self.model.model,
            self.name,
            '%s: %s' % (self.type, self.target.model) if self.target else self.type,
            ' through: (%s)' % self.through if self.through else ''
        )

    def __repr__(self):
        return '<AvailableField "%s" %s.%s (%s)%s>' % (
            self.id,
            self.model.model,
            self.name,
            '%s: %s' % (self.type, self.target.model) if self.target else self.type,
            ' through: (%s)' % self.through if self.through else ''
        )

    def __str__(self):
        return "AF%s %s.%s (%s)%s" % (
            self.id,
            self.model.model,
            self.name,
            '%s: %s' % (self.type, self.target.model) if self.target else self.type,
            ' through: AF#%s' % self.through_id if self.through_id else ''
        )

    def path_for(self, model):
        af = self
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
            if af.model != model:
                logger.error("Failed to generate path for %s relative to %s. Result was %s.%s (%s)", self, model, af.model, label, af)
            #    return u"!!! %s.%s -- %s" % (
            #        af.model,
            #        label,
            #        af
            #    )
            #else:
            return label
    def XXX_simple(self, *a):
        pass

    @staticmethod
    def XXX_static():
        pass

    @classmethod
    def XXX_class(cls, asdf=123):
        pass
