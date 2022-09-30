from django.contrib.syndication.views import Feed

from .config.settings import get_description, get_site_url, get_title
from .retriever import ContentItem, get_content_items


class ContentFeed(Feed):
    title = get_title()
    description = get_description()
    site_url = None

    def __init__(self):
        super().__init__()

        self.site_url = get_site_url()
        assert self.site_url, "COLTRANE_SITE_URL in .env or COLTRANE.SITE_URL in settings file is required"

    def items(self):
        return get_content_items()

    def item_title(self, item: ContentItem):
        return item.metadata.get("title")

    def item_description(self, item: ContentItem):
        return item.metadata.get("description")

    def item_link(self, item: ContentItem):
        _self_url = self.site_url

        if _self_url.endswith("/"):
            _self_url = _self_url[:-1]

        link = f"{_self_url}{item.relative_url}"

        return link

    def link(self, obj):
        return self.site_url
