from optparse import make_option
import inspect
import sys

from django.core.management.base import NoArgsCommand
from django.db import connections, router, transaction, models, DEFAULT_DB_ALIAS
from django.utils.importlib import import_module
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.management import update_contenttypes
from django.db.models import get_apps, get_models
from django.db.models.fields.related import RelatedField

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

def prompt_delete_stale(available_fields, interactive, verbosity):
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
                af.delete()
        else:
            if verbosity >= 2:
                print "Stale available fields remain."

def get_or_create(stale_list, cache_list, verbosity, **kwargs):
    afs = filter_by(cache_list, **kwargs)
    if afs:
        af, = afs
        created = False
    else:
        af, created = AvailableField.objects.get_or_create(**kwargs)
    if created:
        if verbosity >= 2:
            print "Adding %s" % af
        cache_list.add(af)
    else:
        if af in stale_list:
            stale_list.remove(af)
    return created

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

        stale_fields = set(AvailableField.objects.select_related(
            'model',
            'target',
            'through__' * conf.ADMIN_CUSTOMIZER_MAX_FIELD_DEPTH
        ))
        all_fields = stale_fields.copy()

        for app in get_apps():
            if isinstance(app, basestring):
                app = import_module(app + '.models')

            update_contenttypes(app, (), verbosity=verbosity, interactive=interactive)

            app_models = get_models(app)
            for klass in app_models:
                opts = klass._meta
                ct = ContentType.objects.get(app_label=opts.app_label,
                                             model=opts.object_name.lower())
                for field_name in opts.get_all_field_names():
                    field, model, direct, mtm = opts.get_field_by_name(field_name)
                    get_or_create(stale_fields, all_fields, verbosity,
                        name = field.name,
                        type = get_type_for(field),
                        target = get_target_for(field),
                        model = ct,
                        through = None,
                    )
                for member_name, member in inspect.getmembers(klass):
                    if inspect.ismethod(member) and member_name not in (
                            '_get_pk_val', '_get_unique_checks', 'clean',
                            'clean_fields', 'delete', 'full_clean', 'save',
                            'save_base', 'validate_unique'):

                        argspec = inspect.getargspec(member)
                        defaults = len(argspec.defaults) if argspec.defaults else 0
                        if len(argspec.args) - defaults == 1 and not member_name.startswith('_'):
                            get_or_create(stale_fields, all_fields, verbosity,
                                name = member_name,
                                model = ct,
                                type = "meth",
                                target = None,
                                through = None,
                            )
        dirty = True
        while dirty:
            dirty = False
            current_fields = all_fields.copy()
            for c, af in enumerate(current_fields):
                if c % 10 == 0:
                    print "\rChecking spanning AFs, %s/%s +%s" % (
                        c,
                        len(current_fields),
                        len(all_fields) - len(current_fields)
                    ),
                    sys.stdout.flush()
                for raf in filter_by(all_fields, target=af.model):
                    if depth(raf) > conf.ADMIN_CUSTOMIZER_MAX_FIELD_DEPTH:
                        continue
                    if get_or_create(stale_fields, all_fields, verbosity,
                        name = af.name,
                        model = af.model,
                        type = af.type,
                        target = af.target,
                        through = raf
                    ):
                        dirty = True
            print


        prompt_delete_stale(stale_fields, interactive, verbosity)

        print "Total field combinations:", AvailableField.objects.count()
