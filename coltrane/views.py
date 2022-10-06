import logging
from typing import Dict, Tuple

from django.http import Http404, HttpRequest
from django.shortcuts import render
from django.utils.cache import patch_response_headers

from .config.cache import ViewCache
from .renderer import RenderedMarkdown, render_markdown


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


def _get_from_cache_if_enabled(slug: str) -> RenderedMarkdown:
    """
    Gets the slug from the cache if it's enabled.
    """

    rendered_markdown = None
    view_cache = ViewCache()

    if view_cache.is_enabled:
        cache_key = f"{view_cache.cache_key_namespace}{slug}"
        cached_value = view_cache.cache.get(cache_key)

        if cached_value:
            rendered_markdown = cached_value

    return rendered_markdown


def _set_in_cache_if_enabled(slug: str, rendered_markdown: RenderedMarkdown) -> None:
    """
    Sets everything in the cache if it's enabled.
    """

    view_cache = ViewCache()

    if view_cache.is_enabled:
        cache_key = f"{view_cache.cache_key_namespace}{slug}"
        view_cache.cache.set(
            cache_key,
            rendered_markdown,
            view_cache.seconds,
        )


def content(request: HttpRequest, slug: str = "index"):
    """
    Renders the markdown file stored in `content` based on the slug from the URL.
    Adds data into the context from `data.json` and JSON files in the `data` directory.
    Will cache the rendered content if enabled.
    """

    slug = _normalize_slug(slug)
    rendered_markdown = _get_from_cache_if_enabled(slug)

    try:
        if not rendered_markdown:
            rendered_markdown = render_markdown(slug, request=request)
            _set_in_cache_if_enabled(slug, rendered_markdown)
    except FileNotFoundError:
        try:
            slug_with_index = f"{slug}/index"
            rendered_markdown = render_markdown(slug_with_index, request=request)
            _set_in_cache_if_enabled(slug_with_index, rendered_markdown)
        except FileNotFoundError:
            raise Http404(f"{slug} cannot be found")

    response = render(
        request,
        rendered_markdown.content,
        context=rendered_markdown.metadata,
    )

    view_cache = ViewCache()

    if view_cache.is_enabled:
        patch_response_headers(response, cache_timeout=view_cache.seconds)

    return response
