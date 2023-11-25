import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple

from django.http import FileResponse, Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import select_template
from django.utils.cache import patch_response_headers
from django.utils.timezone import now

from coltrane.config.cache import ViewCache
from coltrane.config.paths import get_file_path
from coltrane.config.settings import get_disable_wildcard_templates
from coltrane.renderer import MarkdownRenderer
from coltrane.retriever import get_data

logger = logging.getLogger(__name__)


@dataclass
class PathRanking:
    """Store a path with its score based on where the wildcard is in the path."""

    path: str

    def __init__(self, path: str):
        self.path = path
        self.score = self.score_path()

    def score_path(self):
        total_score = 0
        path = self.path.replace(".html", "")

        for idx, path_piece in enumerate(path.split("/")):
            path_idx = len(path.split("/")) - idx

            if path_piece == "*":
                # Inflate wildcards to ensure they are sorted as expected
                total_score += path_idx * 100
            else:
                total_score += path_idx

        return total_score

    def __str__(self):
        return f"{self.path} ({self.score})"


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

    template: str = ""
    context: Dict = {}
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


def _sort_potential_templates(template_paths):
    """Sort template paths based on where the wildcard is in the directory."""

    rankings = []

    for path in template_paths:
        rankings.append(PathRanking(path))

    rankings = sorted(rankings, key=lambda r: r.score, reverse=False)

    return [r.path for r in rankings]


def _get_potential_wildcard_templates(slug: str) -> List[str]:
    """Get a list of potential wildcard HTML templates based on the slug."""

    wildcard_paths = []

    slug_pieces = slug.split("/")
    slug_pieces_count = len(slug_pieces)

    for outer_idx, _ in enumerate(slug_pieces):
        for inner_idx, _ in enumerate(slug_pieces):
            new_slug_pieces = []

            if outer_idx == inner_idx:
                new_slug_pieces.extend(slug_pieces[:outer_idx])
                new_slug_pieces.extend("*")
                new_slug_pieces.extend(slug_pieces[outer_idx + 1 :])

                wildcard_paths.append(new_slug_pieces)
            elif outer_idx < inner_idx and outer_idx > 0:
                new_slug_pieces.extend(slug_pieces[:outer_idx])
                new_slug_pieces.extend("*" * (slug_pieces_count - outer_idx))

                wildcard_paths.append(new_slug_pieces)
            elif outer_idx > inner_idx and (slug_pieces_count - outer_idx - 1) > 0:
                new_slug_pieces.extend("*" * (slug_pieces_count - outer_idx - 1))
                new_slug_pieces.extend(slug_pieces[outer_idx : outer_idx + 1])
                new_slug_pieces.extend("*" * (slug_pieces_count - outer_idx - 1))

                wildcard_paths.append(new_slug_pieces)

    # Add a catch-all for everything
    # Not needed if there are no potential sub-directories
    if slug_pieces_count > 1:
        new_slug_pieces = []

        for _ in range(slug_pieces_count):
            new_slug_pieces.append("*")

        wildcard_paths.insert(0, new_slug_pieces)

    potential_templates = []

    #  Convert the arrays of paths to paths and add to the list of potential templates
    for wildcard_option in wildcard_paths:
        wildcard_option_path = "/".join(wildcard_option)
        wildcard_option_path = f"{wildcard_option_path}.html"

        potential_templates.append(wildcard_option_path)

    potential_templates = _sort_potential_templates(potential_templates)

    return potential_templates


def content(request: HttpRequest, slug: str = "index") -> HttpResponse:
    """
    Renders the markdown file stored in `content` or HTML template based on the slug from the URL.
    Adds data into the context from `data.json` and JSON files in the `data` directory.

    Will cache the rendered content if enabled.
    """

    template: str = ""
    context: Dict = {}
    slug = _normalize_slug(slug)
    slug_with_index = f"{slug}/index"

    (template, context) = _get_from_cache_if_enabled(slug)
    set_in_cache = False

    try:
        if not template or not context:
            set_in_cache = True

            (template, context) = MarkdownRenderer.instance().render_markdown(slug, request=request)
    except FileNotFoundError:
        try:
            (template, context) = MarkdownRenderer.instance().render_markdown(slug_with_index, request=request)
        except FileNotFoundError:
            # Typical templates based on the slug
            potential_templates = [
                f"{slug}.html",
                f"{slug_with_index}.html",
            ]

            if get_disable_wildcard_templates() is False:
                potential_templates.extend(_get_potential_wildcard_templates(slug))

            try:
                found_template = select_template(potential_templates)
                template = found_template.template.name
            except TemplateDoesNotExist:
                raise Http404(f"{slug} cannot be found") from None

            context.update(
                {
                    "data": get_data(),
                    "slug": slug,
                    "template": template,
                    "now": now(),
                }
            )

    if set_in_cache:
        _set_in_cache_if_enabled(slug, template, context)

    response = render(
        request,
        template,
        context=context,
    )

    view_cache = ViewCache()

    if view_cache.is_enabled:
        patch_response_headers(response, cache_timeout=view_cache.seconds)

    return response


def file(request, file_name: str) -> FileResponse:  # noqa: ARG001
    """
    Serves a file from the file path.
    Based on code in https://adamj.eu/tech/2022/01/18/how-to-add-a-favicon-to-your-django-site/#what-the-file-type.
    """

    file_path = get_file_path(file_name)

    if not file_path.exists():
        raise Http404(f"{file_path.name} cannot be found")

    # Don't use context manager to open the file because it will be closed automatically
    # per https://docs.djangoproject.com/en/4.0/ref/request-response/#fileresponse-objects
    file = file_path.open("rb")

    return FileResponse(file)
