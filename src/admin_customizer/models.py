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

def update_available_fields(app, created_models, verbosity=2, **kwargs):
    if isinstance(app, basestring):
        app = import_module(app + '.models')
    update_contenttypes(app, created_models, verbosity=verbosity, **kwargs)

    available_fields = list(AvailableField.objects.filter(model__app_label=app.__name__.split('.')[-2]))
    app_models = get_models(app)
    if not app_models:
        return
    for klass in app_models:
        opts = klass._meta
        ct = ContentType.objects.get(app_label=opts.app_label,
                                     model=opts.object_name.lower())
        for field in opts.fields:
            try:
                af = AvailableField.objects.get_by_field(ct, field)
                available_fields.remove(af)
            except AvailableField.DoesNotExist:
                af = AvailableField.objects.create_by_field(ct, field)
                if verbosity >= 2:
                    print "Adding %s" % af
    if available_fields:
        if kwargs.get('interactive', False):
            display = '\n'.join(['    %s' % af for af in available_fields])
            ok_to_delete = raw_input("""The following available fields do not exist anymore and need to be deleted:

%s

Any admins using this fields will be affected (they will be removed from them).

    Type 'yes' to continue, or 'no' to cancel: """ % display)
        else:
            ok_to_delete = False

        if ok_to_delete == 'yes':
            for af in available_fields:
                if verbosity >= 2:
                    print "Deleting stale %s" % af
                ct.delete()
        else:
            if verbosity >= 2:
                print "Stale available fields remain."

signals.post_syncdb.connect(update_available_fields)

try:
    from south.signals import post_migrate
except ImportError:
    pass
else:
    def south_update_available_fields(app, **kwargs):
        interactive = False
        frame = sys._getframe(1)
        while frame:
            if frame.f_code.co_name == 'migrate_app':
                if 'interactive' in frame.f_locals:
                    interactive = frame.f_locals['interactive']
                    break
            frame = frame.f_back
        update_available_fields(app, (), interactive=interactive, **kwargs)
    post_migrate.connect(south_update_available_fields)

class AdminSite(models.Model):
    slug = models.SlugField()


class RegisteredModel(models.Model):
    model = models.ForeignKey("contenttypes.ContentType")
    list_display = models.ManyToManyField(
        "AvailableField",
        related_name = "registeredmodels_with_list_display"
    )
    list_filter = models.ManyToManyField(
        "AvailableField",
        related_name = "registeredmodels_with_list_filter"
    )
    search_fields = models.ManyToManyField(
        "AvailableField",
        related_name = "registeredmodels_with_search_fields"
    )
    raw_id_fields = models.ManyToManyField("AvailableField",
        related_name = "registeredmodels_with_",
        limit_choices_to = {'type__in': ('oto', 'fk', 'mtm')}
    )

class AvailableField(models.Model):
    model = models.ForeignKey("contenttypes.ContentType")
    name = models.TextField()
    TYPES = (
        ('fk', _("Foreign key field")),
        ('mtm', _("Many to many field")),
        ('oto', _("One to one field")),
        ('other', _("Other type of field"))
    )
    type = models.CharField(max_length=10, choices=TYPES)

    objects = AvailableFieldManager()

    def __str__(self):
        return "AvailableField '%s | %s | %s'" % (
            self.model,
            self.name,
            self.type
        )
