from datetime import datetime
from typing import Optional

from django.contrib.syndication.views import Feed

from coltrane.config.settings import get_config, get_description, get_site_url, get_title
from coltrane.retriever import ContentItem, get_content_items


class ContentFeed(Feed):
    title = get_title()
    description = get_description()
    _request = None

    def get_feed(self, obj, request):
        self._request = request

        return super().get_feed(obj, request)

    @property
    def site_url(self):
        site_url = get_site_url()

        if not site_url:
            raise AssertionError("COLTRANE_SITE_URL in .env or COLTRANE.SITE_URL in settings file is required")

        return site_url

    def items(self):
        site = None

        if self._request:
            site = get_config().get_site(self._request)

        return get_content_items(site=site)

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

    def item_pubdate(self, item: ContentItem) -> Optional[datetime]:
        if publish_date := item.metadata.get("publish_date"):
            return publish_date

    def link(self, obj):  # noqa: ARG002
        return self.site_url
