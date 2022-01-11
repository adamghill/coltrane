import logging
from typing import Dict, Tuple

from django.http import Http404, HttpRequest
from django.shortcuts import render
from django.utils.cache import patch_response_headers

from .config.cache import ViewCache
from .renderer import render_markdown


logger = logging.getLogger(__name__)


def _normalize_slug(slug: str) -> str:
    if slug is None:
        slug = ""

    if slug.endswith("/"):
        slug = slug[:-1]

    if slug.startswith("/"):
        slug = slug[1:]

    if slug == "":
        slug = "index"

    return slug


def _get_from_cache_if_enabled(slug: str) -> Tuple[str, Dict]:
    """
    Gets the slug from the cache if it's enabled.
    """

    template = None
    context = None
    view_cache = ViewCache()

    if view_cache.is_enabled:
        cache_key = f"{view_cache.cache_key_namespace}{slug}"
        cached_value = view_cache.cache.get(cache_key)

        if cached_value:
            (template, context) = cached_value

    return (template, context)


def _set_in_cache_if_enabled(slug: str, template: str, context: Dict) -> None:
    """
    Sets everything in the cache if it's enabled.
    """

    view_cache = ViewCache()

    if view_cache.is_enabled:
        cache_key = f"{view_cache.cache_key_namespace}{slug}"
        view_cache.cache.set(
            cache_key,
            (template, context),
            view_cache.seconds,
        )


def content(request: HttpRequest, slug: str = "index"):
    """
    Renders the markdown file stored in `content` based on the slug from the URL.
    Adds data into the context from `data.json` and JSON files in the `data` directory.
    Will cache the rendered content if enabled.
    """

    template = ""
    context = {}
    slug = _normalize_slug(slug)

    (template, context) = _get_from_cache_if_enabled(slug)

    try:
        if not template or not context:
            (template, context) = render_markdown(slug, request=request)
            _set_in_cache_if_enabled(slug, template, context)
    except FileNotFoundError:
        raise Http404(f"{slug} cannot be found")

    response = render(
        request,
        template,
        context=context,
    )

    view_cache = ViewCache()

    if view_cache.is_enabled:
        patch_response_headers(response, cache_timeout=view_cache.seconds)

    return response
