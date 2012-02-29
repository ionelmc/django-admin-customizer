from django.utils.translation import ugettext_lazy as _

available_actions = []

def register(func):
    if func not in available_actions:
        available_actions.append(func)
    return func

@register
def export_as_csv(modeladmin, request, queryset, header=True):
    """
    Generic csv export admin action.
    based on http://djangosnippets.org/snippets/1697/
    """
    opts = modeladmin.model._meta
    field_names = set([field.name for field in opts.fields])

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '-')

    writer = csv.writer(response)
    if header:
        writer.writerow(list(field_names))
    def output(obj, field):
        out = getattr(obj, "get_%s_display" % field, None)
        if out:
            out = out()
        else:
            out = getattr(obj, field, None)
        return unicode(out).encode("utf-8","replace")

    for obj in queryset:
        writer.writerow([output(obj, field) for field in field_names])
    return response

export_as_csv.description = _("Export selected objects as CSV file")
