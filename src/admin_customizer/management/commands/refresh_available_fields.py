from optparse import make_option
from django.core.management.base import NoArgsCommand
from django.db import connections, router, transaction, models, DEFAULT_DB_ALIAS
from django.utils.importlib import import_module
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.management import update_contenttypes
from django.db.models import get_apps, get_models

from admin_customizer.models import AvailableField
from admin_customizer import conf

def filter_by(list, **kwargs):
    ret = []
    for el in list:
        ok = True
        for name, value in kwargs.items():
            el_value = getattr(el, name)
            if el_value != value :
                ok = False
                break
        if ok:
            ret.append(el)
    return ret

def depth(af, current=1):
    if not af.through or current > conf.ADMIN_CUSTOMIZER_MAX_FIELD_DEPTH:
        return current
    else:
        return depth(af.through, current+1)

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a database to use. '
                'Defaults to the "default" database.'),
    )
    help = "Create the database tables for all apps in INSTALLED_APPS whose tables haven't already been created."

    def handle_noargs(self, **options):

        verbosity = int(options.get('verbosity', 1))
        interactive = options.get('interactive')
        show_traceback = options.get('traceback', False)

        AvailableField.objects.all().delete()
        available_fields = list(AvailableField.objects.all())

        current_available_fields = []
        for app in get_apps():
            if isinstance(app, basestring):
                app = import_module(app + '.models')

            update_contenttypes(app, (), verbosity=verbosity, interactive=interactive)

            app_models = get_models(app)
            for klass in app_models:
                opts = klass._meta
                ct = ContentType.objects.get(app_label=opts.app_label,
                                             model=opts.object_name.lower())
                for field in opts.fields:
                    af, created = AvailableField.objects.get_or_create_by_field(ct, field)
                    if created:
                        if verbosity >= 2:
                            print "Adding %s" % af
                    else:
                        available_fields.remove(af)
                    current_available_fields.append(af)

        dirty = True
        while dirty:
            dirty = False
            for af in list(current_available_fields):
                #if af.type in AvailableField.RELATION_TYPES:
                for raf in [i for i in current_available_fields if i.target == af.model]:
                    if depth(raf) > conf.ADMIN_CUSTOMIZER_MAX_FIELD_DEPTH:
                        continue
                    args = dict(
                        name = af.name,
                        model = af.model,
                        type = af.type,
                        target = af.target,
                        through = raf
                    )
                    if filter_by(current_available_fields, **args):
                        continue
                    naf, created = AvailableField.objects.get_or_create(**args)
                    if created:
                        if verbosity >= 2:
                            print "Adding %s" % af
                        dirty = True
                    else:
                        if af in available_fields:
                            available_fields.remove(af)
                    current_available_fields.append(naf)

        if available_fields:
            if interactive:
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

        for i in list(AvailableField.objects.all()):
            print i
