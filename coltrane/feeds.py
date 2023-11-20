from django.contrib.syndication.views import Feed

from coltrane.config.settings import get_description, get_site_url, get_title
from coltrane.retriever import ContentItem, get_content_items


class ContentFeed(Feed):
    title = get_title()
    description = get_description()

    @property
    def site_url(self):
        site_url = get_site_url()

        if not site_url:
            raise AssertionError("COLTRANE_SITE_URL in .env or COLTRANE.SITE_URL in settings file is required")

        return site_url

    def items(self):
        return get_content_items()

    def item_title(self, item: ContentItem):
        return item.metadata.get("title")

    def item_description(self, item: ContentItem):
        return item.metadata.get("description")

    def item_link(self, item: ContentItem):
        site_url = self.site_url

        if site_url.endswith("/"):
            site_url = site_url[:-1]

        link = f"{site_url}{item.relative_url}"

        return link

    def link(self, obj):  # noqa: ARG002
        return self.site_url
