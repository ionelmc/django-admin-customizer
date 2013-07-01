from django import VERSION
from django.forms.models import ModelMultipleChoiceField, ModelChoiceIterator
from django.forms.models import ChoiceField, ModelChoiceField
from django.db.models import ManyToManyField
try:
    from django.db import router
except ImportError:
    router = None
from django.db.models import signals
from django.db.models.fields import related

from .widgets import FieldSelect
from . import conf
from .orderedset import OrderedSet

related.OrderedSet = OrderedSet # hax

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
        self.widget = FieldSelect(
            verbose_name,
            enable_ordering = kwargs.pop('enable_ordering', False)
        )
        self.relative_to = relative_to
        super(FieldSelectField, self).__init__(queryset, **kwargs)

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return FieldSelectChoiceIterator(self)
    choices = property(_get_choices, ChoiceField._set_choices)

    def label_from_instance(self, af):
        return af.path_for(self.relative_to)

    def clean(self, value):
        new_value = super(FieldSelectField, self).clean(value)
        mapping = dict((unicode(i.pk), i) for i in new_value)
        return [mapping[pk] for pk in value]

class OrderPreservingManyToManyField(ManyToManyField):
    """
    This field will preserve the database order when fetching from db (via value_from_object)
    and when saving (via the descriptor's _add_items).
    """

    def value_from_object(self, obj):
        "Returns the value of this field in the given model instance."
        if VERSION[:2] >= (1, 2):
            return getattr(obj, self.attname).extra(
                order_by = [self.rel.through._meta.db_table+'.id']
            )
        else:
            raise RuntimeError("Unsupported django version %s." % (VERSION,))

    def contribute_to_class(self, cls, name):
        super(OrderPreservingManyToManyField, self).contribute_to_class(cls, name)
        descriptor = getattr(cls, self.name)
        __get__ = descriptor.__get__
        def get(instance, instance_type=None):
            manager = __get__(instance, instance_type)
            # We want to override the _add_items method in the manager returned by the descriptor
            # However, we cannot create a subclass so we'll patch the returned manager instance
            # instead.

            # The _add_items method from django has 1 free varaibles so we need
            # to bind them outside the scope of the new function
            rel = "hax"
            if VERSION[:2] in ((1, 3), (1, 2)):
                def add_items(self, source_field_name, target_field_name, *objs):
                    # join_table: name of the m2m link table
                    # source_field_name: the PK fieldname in join_table for the source object
                    # target_field_name: the PK fieldname in join_table for the target object
                    # *objs - objects to add. Either object instances, or primary keys of object instances.

                    # If there aren't any objects, there is nothing to do.
                    from django.db.models import Model
                    if objs:
                        new_ids = OrderedSet()
                        for obj in objs:
                            if isinstance(obj, self.model):
                                if not router.allow_relation(obj, self.instance):
                                   raise ValueError('Cannot add "%r": instance is on database "%s", value is on database "%s"' %
                                                       (obj, self.instance._state.db, obj._state.db))
                                new_ids.add(obj.pk)
                            elif isinstance(obj, Model):
                                raise TypeError("'%s' instance expected" % self.model._meta.object_name)
                            else:
                                new_ids.add(obj)
                        db = router.db_for_write(self.through, instance=self.instance)
                        vals = self.through._default_manager.using(db).values_list(target_field_name, flat=True)
                        vals = vals.filter(**{
                            source_field_name: self._pk_val,
                            '%s__in' % target_field_name: new_ids,
                        })
                        new_ids = new_ids - set(vals)

                        if self.reverse or source_field_name == self.source_field_name:
                            # Don't send the signal when we are inserting the
                            # duplicate data row for symmetrical reverse entries.
                            signals.m2m_changed.send(sender=rel.through, action='pre_add',
                                instance=self.instance, reverse=self.reverse,
                                model=self.model, pk_set=new_ids, using=db)
                        # Add the ones that aren't there already
                        for obj_id in new_ids:
                            self.through._default_manager.using(db).create(**{
                                '%s_id' % source_field_name: self._pk_val,
                                '%s_id' % target_field_name: obj_id,
                            })
                        if self.reverse or source_field_name == self.source_field_name:
                            # Don't send the signal when we are inserting the
                            # duplicate data row for symmetrical reverse entries.
                            signals.m2m_changed.send(sender=rel.through, action='post_add',
                                instance=self.instance, reverse=self.reverse,
                                model=self.model, pk_set=new_ids, using=db)
            elif VERSION[:2] in ((1, 4), (1, 5), (1, 6)):
                def add_items(self, source_field_name, target_field_name, *objs):
                    # source_field_name: the PK fieldname in join table for the source object
                    # target_field_name: the PK fieldname in join table for the target object
                    # *objs - objects to add. Either object instances, or primary keys of object instances.

                    # If there aren't any objects, there is nothing to do.
                    from django.db.models import Model
                    if objs:
                        new_ids = OrderedSet()
                        for obj in objs:
                            if isinstance(obj, self.model):
                                if not router.allow_relation(obj, self.instance):
                                   raise ValueError('Cannot add "%r": instance is on database "%s", value is on database "%s"' %
                                                       (obj, self.instance._state.db, obj._state.db))
                                new_ids.add(obj.pk)
                            elif isinstance(obj, Model):
                                raise TypeError("'%s' instance expected, got %r" % (self.model._meta.object_name, obj))
                            else:
                                new_ids.add(obj)
                        db = router.db_for_write(self.through, instance=self.instance)
                        vals = self.through._default_manager.using(db).values_list(target_field_name, flat=True)
                        if hasattr(self, '_fk_val'):
                            _pk_val = self._fk_val
                        else:
                            _pk_val = self._pk_val
                        vals = vals.filter(**{
                            source_field_name: _pk_val,
                            '%s__in' % target_field_name: new_ids,
                        })
                        new_ids = new_ids - set(vals)

                        if self.reverse or source_field_name == self.source_field_name:
                            # Don't send the signal when we are inserting the
                            # duplicate data row for symmetrical reverse entries.
                            signals.m2m_changed.send(sender=self.through, action='pre_add',
                                instance=self.instance, reverse=self.reverse,
                                model=self.model, pk_set=new_ids, using=db)
                        # Add the ones that aren't there already
                        for obj_id in new_ids:
                            self.through._default_manager.using(db).create(**{
                                '%s_id' % source_field_name: _pk_val,
                                '%s_id' % target_field_name: obj_id,
                            })

                        if self.reverse or source_field_name == self.source_field_name:
                            # Don't send the signal when we are inserting the
                            # duplicate data row for symmetrical reverse entries.
                            signals.m2m_changed.send(sender=self.through, action='post_add',
                                instance=self.instance, reverse=self.reverse,
                                model=self.model, pk_set=new_ids, using=db)
            else:
                raise RuntimeError("Unsupported django version %s." % (VERSION,))
            manager._add_items.im_func.func_code = add_items.func_code # now we can safely patch it
                                                                       # (number of free variables match)
            return manager
        descriptor.__get__ = get
