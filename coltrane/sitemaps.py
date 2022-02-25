from django.contrib.sitemaps import Sitemap

from coltrane.retriever import get_content_paths


class ContentSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5

    def items(self):
        return list(get_content_paths())

    def location(self, obj):
        relative_url = str(obj)[7:-3]

        if relative_url.endswith("/index"):
            relative_url = relative_url[:-6]

        return relative_url
