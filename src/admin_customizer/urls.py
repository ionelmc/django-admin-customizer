from django.conf.urls.defaults import patterns, url, include
from django.contrib.admin import AdminSite as DjangoAdminSite, ModelAdmin

from .models import get_active_models, RegisteredModel

urlpatterns = patterns("admin_customizer.views",
    url('^$', 'admin_index', name="admin_customizer-admin_index"),
)
active_models, checksum = get_active_models()

list_display_through = RegisteredModel._meta.get_field_by_name(
    "list_display")[0].rel.through._meta.db_table

for slug, models in active_models.items():
    admin_site = DjangoAdminSite(name=slug, app_name=slug)
    for registered_model in models:
        ct = registered_model.model
        DynamicModelAdmin = type(
            str("%(site_name)s_%(app_label)s_%(model_name)s_Admin" % dict(
                site_name = slug,
                app_label = ct.app_label,
                model_name = ct.model,
            )),
            (ModelAdmin,),
            dict(
                list_display = [
                    field.name for field in registered_model.list_display.extra(
                        order_by = [list_display_through+'.id']
                    )
                ],
                list_filter = [
                    field.name for field in registered_model.list_filter.all()
                ],
                search_fields = [
                    field.name for field in registered_model.search_fields.all()
                ],
                raw_id_fields = [
                    field.name for field in registered_model.raw_id_fields.all()
                ],
            )
        )
        admin_site.register(
            ct.model_class(),
            DynamicModelAdmin
        )
    urlpatterns.append(url('^%s/' % slug, include(admin_site.urls)))
