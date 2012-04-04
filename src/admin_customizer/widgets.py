from itertools import chain

from django.conf import settings
from django import forms
from django.forms.widgets import Widget
from django.template.defaulttags import mark_safe
from django.template.defaultfilters import force_escape
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
try:
    from django.utils.html import escapejs
except ImportError:
    from django.template.defaultfilters import escapejs

from . import conf
from .orderedset import OrderedSet

class NotAnInput(Widget):
    """
    Base class for all <input> widgets (except type='checkbox' and
    type='radio', which are special).
    """
    def _format_value(self, value):
        return unicode(value)

    def render(self, name, value, attrs=None):
        return mark_safe('<span class="not-an-input">%s</span>' % force_escape(value)) if value else ''

class FieldSelect(forms.SelectMultiple):
    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + "js/core.js",
            settings.ADMIN_MEDIA_PREFIX + "js/SelectBox.js",
            'admin_customizer/widgets/jquery-1.7.1.min.js',
            'admin_customizer/widgets/field-select.js',
        )
        css = {
            'all': (
                'admin_customizer/widgets/field-select.css',
            )
        }
    def __init__(self, verbose_name, attrs=None, choices=(), enable_ordering=False):
        self.verbose_name = verbose_name
        self.enable_ordering = enable_ordering
        super(FieldSelect, self).__init__(attrs, choices)

    def render_option(self, selected_choices, option_value, option_label,
                      selected):
        option_value = force_unicode(option_value)
        selected_html = selected and u' selected="selected"' or ''
        # Disabled for now, should reenable later if all the m2m widgets are changed to this
        return u'<option value="%s" data-label="%s" data-parent="%s"%s>%s</option>' % (
            escape(option_value),
            escape(option_label.label),
            escape(option_label.parent or ''),
            selected_html,
            conditional_escape(force_unicode(option_label.verbose_label)))

    def render_options(self, choices, selected_choices):
        selected_choices = OrderedSet([
            force_unicode(v) for v in selected_choices
        ])
        output = []
        options = dict(
            (force_unicode(value), label)
            for value, label in chain(self.choices, choices)
        )
        for option_value in selected_choices:
            if option_value in options:
                option_label = options[option_value]
                output.append(self.render_option(
                    selected_choices, option_value, option_label, True))

        for option_value, option_label in chain(self.choices, choices):
            option_value = str(option_value)
            if option_value not in selected_choices:
                output.append(self.render_option(
                    selected_choices, option_value, option_label, False))
        return u'\n'.join(output)

    def render(self, name, value, attrs=None, choices=()):
        if attrs is None: attrs = {}
        attrs['class'] = 'field-selectfilter'
        output = [super(FieldSelect, self).render(name, value, attrs, choices)]
        output.append(u'''
            <script type="text/javascript">$(function() {
                $('#%s').fieldSelect({
                    field_name: '%s',
                    admin_media: '%s',
                    max_levels: %s,
                    add_parents: false,
                    enable_ordering: %s
                });
            });</script>
        ''' % (
            attrs['id'],
            escapejs(self.verbose_name),
            settings.ADMIN_MEDIA_PREFIX,
            conf.MAX_FIELD_DEPTH,
            'true' if self.enable_ordering else 'false'
        ))
        return mark_safe(u''.join(output))
