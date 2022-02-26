from pathlib import Path

from django.contrib.sitemaps import Sitemap

from coltrane.renderer import render_markdown_path
from coltrane.retriever import get_content_paths


class ContentSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5

    def items(self):
        # TODO: This could get cached so it isn't re-generated every time
        paths = get_content_paths()
        _items = []

        for path in paths:
            (_, metadata) = render_markdown_path(path)

            if "draft" in metadata:
                if metadata["draft"]:
                    continue

            _items.append(path)

        return _items

    def location(self, path: Path):
        relative_url = str(path)[7:-3]

        if relative_url.endswith("/index"):
            relative_url = relative_url[:-6]

        return relative_url
