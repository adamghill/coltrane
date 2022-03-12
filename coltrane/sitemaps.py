from pathlib import Path

from django.contrib.sitemaps import Sitemap

from coltrane.config.paths import get_content_directory
from coltrane.renderer import render_markdown_path
from coltrane.retriever import get_content_paths


class ContentSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5

    MARKDOWN_EXTENSION_LENGTH = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # used to get a relative URL, but only needs to be calculated
        # when the class is instantiated
        content_directory = get_content_directory()
        self.content_directory_path_length = len(str(content_directory))

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

    def _get_relative_url(self, path: Path):
        path_str = str(path)
        relative_url = path_str[
            self.content_directory_path_length : -self.MARKDOWN_EXTENSION_LENGTH
        ]

        return relative_url

    def location(self, path: Path):
        relative_url = self._get_relative_url(path)

        if relative_url.endswith("/index"):
            relative_url = relative_url[:-6]

        return relative_url
