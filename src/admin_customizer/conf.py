from django.conf import settings

ADMIN_CUSTOMIZER_MAX_FIELD_DEPTH = getattr(settings, 'ADMIN_CUSTOMIZER_MAX_FIELD_DEPTH', 5)
