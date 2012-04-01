from django.conf import settings

MAX_FIELD_DEPTH = getattr(
    settings, 'ADMIN_CUSTOMIZER_MAX_FIELD_DEPTH', 5)
URL_RELOADER_CACHE_KEY = getattr(
    settings,
    'ADMIN_CUSTOMIZER_URL_RELOADER_CACHE_KEY',
    'admin-customizer-urls-checksum')
URL_RELOADER_ENABLED = (
    'admin_customizer.middleware.URLResolverReloadMiddleware'
        in settings.MIDDLEWARE_CLASSES
)
