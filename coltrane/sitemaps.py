from pathlib import Path

from django.contrib.sitemaps import Sitemap

from coltrane.retriever import get_content_paths


class ContentSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5

    def items(self):
        # TODO: This could get cached so it isn't re-generated every time
        return list(get_content_paths())

    def location(self, path: Path):
        relative_url = str(path)[7:-3]

        if relative_url.endswith("/index"):
            relative_url = relative_url[:-6]

        return relative_url
