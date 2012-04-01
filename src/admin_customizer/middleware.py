from logging import getLogger
logger = getLogger(__name__)

from django.core.cache import cache
from django.core.urlresolvers import clear_url_caches

from . import urls
from . import conf

def reload_urls():
    logger.info("Reloading %s", urls)
    reload(urls)
    clear_url_caches()

class URLResolverReloadMiddleware(object):
    def process_request(self, request):
        checksum = cache.get(conf.URL_RELOADER_CACHE_KEY)
        if urls.checksum != checksum:
            reload_urls()

