from typing import Dict

from django import template

from coltrane.renderer import get_html_and_markdown
from coltrane.retriever import get_content_paths


register = template.Library()


@register.simple_tag(takes_context=True)
def directory_contents(context, directory: str = None) -> Dict[str, str]:
    if not directory:
        request = context["request"]
        directory = request.path

        if directory.startswith("/"):
            directory = directory[1:]

    content_paths = get_content_paths(directory)
    contents = []

    for path in content_paths:
        if path.name != "index.md":
            path_slug = path.name[:-3]

            content_slug = path_slug

            if directory:
                content_slug = f"{directory}/{path_slug}"

            (_, metadata) = get_html_and_markdown(content_slug)
            title = metadata.get("title")

            contents.append({"slug": content_slug, "title": title})

    return contents
