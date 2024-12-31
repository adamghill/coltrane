import logging

from django.contrib.sitemaps.views import _get_latest_lastmod, x_robots_tag
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import FileResponse, Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import select_template
from django.template.response import TemplateResponse
from django.utils.cache import patch_response_headers
from django.utils.http import http_date
from django.utils.timezone import now

from coltrane.config.cache import ViewCache
from coltrane.config.paths import get_file_path
from coltrane.config.settings import get_config, get_disable_wildcard_templates
from coltrane.renderer import MarkdownRenderer
from coltrane.retriever import get_data
from coltrane.sitemaps import ContentSitemap
from coltrane.wildcard_templates import get_potential_wildcard_templates

# logging.basicConfig(level=logging.DEBUG)
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


def _get_from_cache_if_enabled(slug: str) -> tuple[str, dict]:
    """
    Gets the slug from the cache if it's enabled.
    """

    template: str = ""
    context: dict = {}
    view_cache = ViewCache()

    if view_cache.is_enabled:
        cache_key = f"{view_cache.cache_key_namespace}{slug}"
        cached_value = view_cache.cache.get(cache_key)

        if cached_value:
            (template, context) = cached_value

    return (template, context)


def _set_in_cache_if_enabled(slug: str, template: str, context: dict) -> None:
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


def _render_markdown_for_potential_slugs(potential_slugs: list[str], request: HttpRequest):
    for slug in potential_slugs:
        try:
            (template, context) = MarkdownRenderer.instance().render_markdown(slug, request=request)

            return (template, context)
        except FileNotFoundError:
            pass

    raise FileNotFoundError()


def content(request: HttpRequest, slug: str = "index") -> HttpResponse:
    """Renders the markdown file stored in `content` or HTML template based on the slug from the URL.
    Adds data into the context from JSON files in the `data` directory.

    Will cache the rendered content if enabled.
    """

    logger.debug(f"request: {request}")

    config = get_config()
    site = config.get_site(request)
    logger.debug(f"site: {site}")
    logger.debug(f"base_dir {config.base_dir}")

    template: str = ""
    context: dict = {}
    slug = _normalize_slug(slug)
    slug_with_index = f"{slug}/index"

    (template, context) = _get_from_cache_if_enabled(slug)
    set_in_cache = False

    try:
        if not template or not context:
            set_in_cache = True
            potential_slugs = []

            potential_slugs.extend([slug, slug_with_index])
            logger.debug(f"potential_slugs: {potential_slugs}")

            (template, context) = _render_markdown_for_potential_slugs(potential_slugs=potential_slugs, request=request)

            template = site.get_template_name(template_name=template, verify=True)
    except FileNotFoundError:
        potential_templates = []

        if site and site.is_custom:
            potential_templates.extend(
                [
                    f"{site.folder}/templates/{slug}.html",
                    f"{site.folder}/templates/{slug_with_index}.html",
                ]
            )

        # Typical templates based on the slug
        potential_templates.extend([f"{slug}.html", f"{slug_with_index}.html"])

        if get_disable_wildcard_templates() is False:
            potential_wildcard_templates = get_potential_wildcard_templates(slug)

            if site and site.is_custom:
                potential_wildcard_templates = [f"{site.folder}/templates/{t}" for t in potential_wildcard_templates]
                potential_templates.extend(potential_wildcard_templates)
            else:
                potential_templates.extend(potential_wildcard_templates)

        # from django.conf import settings

        # print("settings.tempaltes", settings.TEMPLATES)
        # print("settings.base_dir", settings.BASE_DIR)
        # print(f"potential_templates: {potential_templates}")

        try:
            # potential_templates.insert(0, "sites/adamghill/templates/index.html")
            logger.debug(f"potential_templates: {potential_templates}")
            selected_template = select_template(potential_templates)

            logger.debug(f"selected_template: {selected_template}")
            template = selected_template.template.name
            logger.debug(f"template: {template}")
        except TemplateDoesNotExist:
            raise Http404(f"{slug} cannot be found") from None

        context.update(
            {
                "data": get_data(site=site),
                "slug": slug,
                "template": template,
                "now": now(),
            }
        )

    if set_in_cache:
        _set_in_cache_if_enabled(slug, template, context)

    context["site"] = str(site) if site else None

    logger.debug(f"template: {template}")

    response = render(
        request,
        template,
        context=context,
    )

    view_cache = ViewCache()

    if view_cache.is_enabled:
        patch_response_headers(response, cache_timeout=view_cache.seconds)

    return response


def file(request, file_name: str) -> FileResponse:
    """Serves a file from the file path.

    Based on code in https://adamj.eu/tech/2022/01/18/how-to-add-a-favicon-to-your-django-site/#what-the-file-type.
    """

    config = get_config()
    site = config.get_site(request)

    file_path = get_file_path(site=site, file_name=file_name)

    if not file_path.exists():
        raise Http404(f"{file_path.name} cannot be found")

    # Don't use context manager to open the file because it will be closed automatically
    # per https://docs.djangoproject.com/en/4.0/ref/request-response/#fileresponse-objects
    file = file_path.open("rb")

    return FileResponse(file)


def healthcheck(request) -> JsonResponse:  # noqa: ARG001
    """Serves a JSON response if the site is up and running."""

    return JsonResponse({"status": "ok"})


@x_robots_tag
def sitemap(request):
    """Returns a sitemap for all of the content for the current site.

    Based heavily on django.contrib.sitemaps.views.sitemap.
    """

    template_name = "sitemap.xml"
    content_type = "application/xml"

    req_protocol = request.scheme
    req_site = get_current_site(request)

    page = request.GET.get("p", 1)

    lastmod = None
    all_sites_lastmod = True
    urls = []

    try:
        config = get_config()
        site = config.get_site(request)

        content_sitemap = ContentSitemap()
        content_sitemap.site = site

        urls.extend(content_sitemap.get_urls(page=page, site=req_site, protocol=req_protocol))

        if all_sites_lastmod:
            site_lastmod = getattr(content_sitemap, "latest_lastmod", None)

            if site_lastmod is not None:
                lastmod = _get_latest_lastmod(lastmod, site_lastmod)
            else:
                all_sites_lastmod = False
    except EmptyPage as e:
        raise Http404(f"Page {page} empty") from e
    except PageNotAnInteger as e:
        raise Http404(f"No page '{page}'") from e

    # If lastmod is defined for all sites, set header so as
    # ConditionalGetMiddleware is able to send 304 NOT MODIFIED
    if all_sites_lastmod:
        headers = {"Last-Modified": http_date(lastmod.timestamp())} if lastmod else None
    else:
        headers = None

    return TemplateResponse(
        request,
        template_name,
        {"urlset": urls},
        content_type=content_type,
        headers=headers,
    )
