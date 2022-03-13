from django.contrib.sitemaps import Sitemap

from coltrane.retriever import ContentItem, get_content_items


class ContentSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5

    def items(self):
        return get_content_items()

    def location(self, content_item: ContentItem) -> str:
        return content_item.relative_url
