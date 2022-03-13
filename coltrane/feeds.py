from django.contrib.syndication.views import Feed

from .config.settings import get_description, get_site, get_title
from .retriever import ContentItem, get_content_items


class ContentFeed(Feed):
    title = get_title()
    description = get_description()

    def items(self):
        return get_content_items()

    def item_title(self, item: ContentItem):
        return item.metadata.get("title")

    def item_description(self, item: ContentItem):
        return item.metadata.get("description")

    def item_link(self, item: ContentItem):
        site = get_site()
        assert site, "COLTRANE_SITE is required in .env"

        if site.endswith("/"):
            site = site[:-1]

        link = f"{site}{item.relative_url}"

        return link

    def link(self, obj):
        site = get_site()
        assert site, "COLTRANE_SITE is required in .env"

        return site
