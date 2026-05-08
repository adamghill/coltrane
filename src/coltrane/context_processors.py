from django.conf import settings

from coltrane.config.settings import get_config


def coltrane(request):
    coltrane_settings = settings.COLTRANE.copy()

    if hasattr(request, "site"):
        site = request.site
    else:
        site = get_config().get_site(request)

    if site:
        if site.title:
            coltrane_settings["TITLE"] = site.title

        if site.description:
            coltrane_settings["DESCRIPTION"] = site.description

        if site.site_url:
            coltrane_settings["SITE_URL"] = site.site_url

        if site.data:
            coltrane_settings["DATA"] = site.data

    return {
        "coltrane_config": coltrane_settings,
    }
