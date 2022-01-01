import logging

from django.http import Http404, HttpRequest
from django.shortcuts import render

from .renderer import render_markdown


logger = logging.getLogger(__name__)


def content(request: HttpRequest, slug: str = "index"):
    """
    Renders the markdown file stored in `content` based on the slug from the URL. Adds data into the context
    from `data.json` and JSON files in the `data` directory.
    """

    try:
        (content, data) = render_markdown(slug)

        return render(
            request,
            "static_site/content.html",
            context={"content": content, "data": data},
        )
    except FileNotFoundError:
        raise Http404(f"{slug} cannot be found")
