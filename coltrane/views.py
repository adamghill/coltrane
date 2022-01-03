import logging

from django.conf import settings
from django.core.cache import cache
from django.http import Http404, HttpRequest
from django.shortcuts import render
from django.utils.html import mark_safe  # type: ignore

from .renderer import render_markdown


logger = logging.getLogger(__name__)


DEFAULT_VIEW_CACHE_SECONDS = 60 * 60


def _get_view_cache_seconds() -> int:
    """
    Get the view cache seconds from settings or just send back the default of an hour.
    """

    if hasattr(settings, "COLTRANE") and isinstance(settings.COLTRANE, dict):
        return settings.COLTRANE.get("VIEW_CACHE_SECONDS", DEFAULT_VIEW_CACHE_SECONDS)

    return DEFAULT_VIEW_CACHE_SECONDS


def content(request: HttpRequest, slug: str = "index"):
    """
    Renders the markdown file stored in `content` based on the slug from the URL. Adds data into the context
    from `data.json` and JSON files in the `data` directory.
    """

    content = ""
    data = {}

    # Cache the rendered content via the low-level API.
    # TODO: Use the `cache_page` decorator and figure out why the settings error is thrown.
    # TODO: Use `django.views.decorators.http.condition` decorator for proper Etags
    cache_key = f"coltron:{slug}"

    if not settings.DEBUG:
        cached_value = cache.get(cache_key)

        if cached_value:
            (content, data) = cached_value

    try:
        if not content:
            (content, data) = render_markdown(slug)

            if not settings.DEBUG:
                cache.set(
                    cache_key,
                    (content, data),
                    _get_view_cache_seconds(),
                )
    except FileNotFoundError:
        raise Http404(f"{slug} cannot be found")

    return render(
        request,
        "coltrane/content.html",
        context={"content": mark_safe(content), "data": data},
    )
