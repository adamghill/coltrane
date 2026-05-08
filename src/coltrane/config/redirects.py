from collections.abc import Generator
from typing import TYPE_CHECKING

import msgspec

from coltrane.config.settings import get_config

if TYPE_CHECKING:
    from coltrane.config.coltrane import Site


class Redirect(msgspec.Struct):
    """Data for a redirect"""

    to_url: str | None = msgspec.field(name="url")
    permanent: bool = False
    from_url: str = ""


def get_redirects() -> Generator[Redirect, None, None]:
    """Yield redirects from coltrane.toml configuration"""
    for redirect in get_config().redirects:
        from_url = redirect.from_url

        if from_url.startswith("/"):
            from_url = from_url[1:]

        yield Redirect(from_url=from_url, to_url=redirect.to_url, permanent=redirect.permanent)


def get_redirect(path: str, site: "Site | None" = None) -> Redirect | None:
    if path.startswith("/"):
        path = path[1:]

    # Check site-specific redirects first
    if site:
        for redirect in site.redirects:
            if redirect.from_url.strip("/") == path:
                return Redirect(to_url=redirect.to_url, permanent=redirect.permanent, from_url=redirect.from_url)

    # Check global redirects (from coltrane.toml)
    for redirect in get_redirects():
        if redirect.from_url.strip("/") == path:
            return redirect

    return None
