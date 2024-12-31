from typing import TYPE_CHECKING, Optional

from django.contrib.sitemaps import Sitemap

from coltrane.retriever import ContentItem, get_content_items

if TYPE_CHECKING:
    from coltrane.config.coltrane import Site


class ContentSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5
    site: Optional["Site"] = None

    def items(self):
        return get_content_items(site=self.site)

    def location(self, content_item: ContentItem) -> str:
        return content_item.relative_url
