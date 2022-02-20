from typing import Dict

from django import template
from django.utils.safestring import SafeString

from coltrane.renderer import get_html_and_markdown
from coltrane.retriever import get_content_directory, get_content_paths


register = template.Library()


@register.simple_tag(takes_context=True)
def directory_contents(context, directory: str = None) -> Dict[str, str]:
    if not directory:
        request = context["request"]
        directory = request.path

        if directory.startswith("/"):
            directory = directory[1:]
    elif isinstance(directory, SafeString):
        # Force SafeString to be a normal string so it can be used with `Path` later
        directory = directory + ""

    content_paths = get_content_paths(directory)
    contents = []

    for path in content_paths:
        if path.name != "index.md":
            path_slug = path.name[:-3]
            content_slug = path_slug
            content_directory = get_content_directory()

            if directory:
                content_slug = f"{directory}/{path_slug}"
                content_directory = content_directory / directory

            directory_without_name = str(path).replace(path.name, "")[:-1]

            if str(content_directory) != directory_without_name:
                continue

            (_, metadata) = get_html_and_markdown(content_slug)

            contents.append(metadata)

    return contents
