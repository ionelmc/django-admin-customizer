import logging
import logging.handlers

import random
import time

from django import VERSION
from django.test import TestCase
from django import forms

import time
import re

from .models import Book, Author, BookNote
from admin_customizer.models import RegisteredModel, AvailableField, AdminSite
from admin_customizer.fields import FieldSelectField
from django.contrib.contenttypes.models import ContentType

class AssertingHandler(logging.handlers.BufferingHandler):

    def __init__(self,capacity):
        logging.handlers.BufferingHandler.__init__(self,capacity)

    def assertLogged(self, test_case, msg):
        for record in self.buffer:
            s = self.format(record)
            if s.startswith(msg):
                return
        test_case.assertTrue(False, "Failed to find log message: " + msg)

class _AssertRaisesContext(object):
    """A context manager used to implement TestCase.assertRaises* methods."""

    def __init__(self, expected, test_case, expected_regexp=None):
        self.expected = expected
        self.failureException = test_case.failureException
        self.expected_regexp = expected_regexp

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            try:
                exc_name = self.expected.__name__
            except AttributeError:
                exc_name = str(self.expected)
            raise self.failureException(
                "{0} not raised".format(exc_name))
        if not issubclass(exc_type, self.expected):
            # let unexpected exceptions pass through
            return False
        self.exception = exc_value # store for later retrieval
        if self.expected_regexp is None:
            return True

        expected_regexp = self.expected_regexp
        if isinstance(expected_regexp, basestring):
            expected_regexp = re.compile(expected_regexp)
        if not expected_regexp.search(str(exc_value)):
            raise self.failureException('"%s" does not match "%s"' %
                     (expected_regexp.pattern, str(exc_value)))
        return True

class PrefetchTests(TestCase):
    def assertRegexpMatches(self, text, expected_regexp, msg=None):
        """Fail the test unless the text matches the regular expression."""
        if isinstance(expected_regexp, basestring):
            expected_regexp = re.compile(expected_regexp)
        if not expected_regexp.search(text):
            msg = msg or "Regexp didn't match"
            msg = '%s: %r not found in %r' % (msg, expected_regexp.pattern, text)
            raise self.failureException(msg)

    def assertRaises(self, excClass, callableObj=None, *args, **kwargs):
        """Fail unless an exception of class excClass is thrown
           by callableObj when invoked with arguments args and keyword
           arguments kwargs. If a different type of exception is
           thrown, it will not be caught, and the test case will be
           deemed to have suffered an error, exactly as for an
           unexpected exception.

           If called with callableObj omitted or None, will return a
           context object used like this::

                with self.assertRaises(SomeException):
                    do_something()

           The context manager keeps a reference to the exception as
           the 'exception' attribute. This allows you to inspect the
           exception after the assertion::

               with self.assertRaises(SomeException) as cm:
                   do_something()
               the_exception = cm.exception
               self.assertEqual(the_exception.error_code, 3)
        """
        context = _AssertRaisesContext(excClass, self)
        if callableObj is None:
            return context
        with context:
            callableObj(*args, **kwargs)

    def test_ordered_mtm_widget(self):
        book_ct = ContentType.objects.get_for_model(Book)
        class RegModelForm(forms.ModelForm):
            class Meta:
                model = RegisteredModel
                fields = 'list_display',

            list_display = FieldSelectField(
                "list_display",
                Book,
                AvailableField.objects.filter_for_model(model=book_ct).filter(
                    type__in = AvailableField.LIST_DISPLAY_TYPES
                ),
                enable_ordering = True,
            )

        reg_model = RegisteredModel.objects.create(
            model = book_ct,
            admin_site = AdminSite.objects.create(slug='test'),
            active = True
        )
        afs = list(AvailableField.objects.filter_for_model(
            model = book_ct
        ).values_list(
            'id', 'name'
        ).filter(
            type__in = AvailableField.LIST_DISPLAY_TYPES
        ))

        empty_form = RegModelForm(instance=reg_model).as_p()
        expected = '\n'.join(
            '<option value="%s" data-label="%s" data-parent="">%s</option>'%
            (id, name, name) for id, name in afs
        )
        self.assertTrue(
            expected in empty_form, "%r not in %r" % (expected, empty_form)
        )
        new_afs = list(afs)
        random.shuffle(new_afs, lambda: 0.345)

        from django.utils.datastructures import MultiValueDict
        bound_form = RegModelForm(MultiValueDict({
            'list_display': [str(id) for id, name in new_afs],
        }), instance=reg_model)
        self.assertTrue(bound_form.is_valid(), bound_form.errors)
        bound_form.save()

        empty_form = RegModelForm(instance=RegisteredModel.objects.get(id=reg_model.id)).as_p()
        expected = '\n'.join(
            '<option value="%s" data-label="%s" data-parent="" '
            'selected="selected">%s</option>' %
            (id, name, name) for id, name in new_afs
        )
        self.assertTrue(
            expected in empty_form, "%r not in %r" % (expected, empty_form)
        )
