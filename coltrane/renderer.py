import codecs
import logging
import re
from dataclasses import dataclass, field
from html import unescape
from typing import Dict, Optional, Tuple, Union
from urllib.parse import unquote

import dateparser
from django.http import HttpRequest
from django.template import engines
from django.utils.html import mark_safe  # type: ignore
from django.utils.text import slugify
from django.utils.timezone import now
from markdown2 import Markdown, markdown

from coltrane.config.paths import get_content_directory
from coltrane.config.settings import (
    get_markdown_extras,
    get_markdown_renderer,
    get_mistune_plugins,
    get_site_url,
)
from coltrane.retriever import get_data

logger = logging.getLogger(__name__)

DEFAULT_TEMPLATE = "coltrane/content.html"

SPACE_REPLACEMENT = "DJANGO-TEMPLATE-TAG-SPACE"


@dataclass
class StaticRequest(HttpRequest):
    """
    Used to mock an HttpRequest when generating the HTML for static sites.

    Required for `coltrane.templatetags.coltrane.current_direct
    """

    path: str
    META: Dict = field(default_factory=dict)
    GET: Dict = field(default_factory=dict)

    def __init__(self, path: str, meta=None, get=None):
        self.path = path
        self.META = meta or {}
        self.GET = get or {}

    @property
    def site_url(self):
        site_url = get_site_url()

        if not site_url:
            raise AssertionError("COLTRANE_SITE_URL in .env or COLTRANE.SITE_URL in settings file is required")

        return site_url

    @property
    def scheme(self) -> str:
        return str(self.site_url.split("://")[0])

    def get_host(self) -> str:
        return str(self.site_url.split("://")[1])

    def is_secure(self) -> bool:
        return self.path.startswith("https://")


class MarkdownRenderer:
    _instance = None

    def _get_markdown_content_as_html(self, slug: str) -> Tuple[str, Optional[Dict]]:
        """
        Converts markdown file based on the slug into HTML.
        """

        path = get_content_directory() / f"{slug}.md"

        return self.render_markdown_path(path)

    def pre_process_markdown(self, text: str) -> str:
        # Wrap code fences with Django `verbatim` templatetag; these get removed in
        # `post_process_html`
        text = re.sub(
            pattern=r"```.*?```",
            repl="{% verbatim %}\n\\g<0>\n{% endverbatim %}",
            string=text,
            flags=re.RegexFlag.DOTALL,
        )

        return text

    def post_process_html(self, html: str) -> str:
        # Remove `p` tags that get added to the `verbatim` templatetag
        html = html.replace("<p>{% verbatim %}</p>\n", "{% verbatim %}")
        html = html.replace("\n<p>{% endverbatim %}</p>", "{% endverbatim %}")

        return html

    def render_markdown_path(self, path) -> Tuple[str, Dict]:
        """
        Renders the markdown file located at path.
        """

        with codecs.open(path, "r", encoding="utf-8") as f:
            text = f.read()

            return self.render_markdown_text(text)

    def render_markdown_text(self, text: str) -> Tuple[str, Dict]:  # noqa: ARG002
        raise Exception("Missing render_markdown_text")

    def render_html_with_django(self, html: str, context: Dict, request: HttpRequest = None) -> str:
        """
        Takes the rendered HTML from the markdown and use Django to fill in any template
        variables from the `context` dictionary.
        """

        django_engine = engines["django"]
        template = django_engine.from_string(html)

        return str(template.render(context=context, request=request))

    def get_html_and_markdown(self, slug: str) -> Tuple[str, Dict]:
        (html, metadata) = self._get_markdown_content_as_html(slug)

        if metadata is None:
            metadata = {}

        if "template" not in metadata:
            metadata["template"] = DEFAULT_TEMPLATE

        metadata["slug"] = slug

        return (html, metadata)

    def render_markdown(
        self,
        slug: str,
        request: Union[HttpRequest, StaticRequest],
    ) -> Tuple[str, Dict]:
        """
        Renders the markdown from the `slug` by:
        1. Rendering the markdown file into HTML
        2. Passing the HTML through Django to fill in template variables based on
            data in JSON files and markdown frontmatter

        Returns:
            Tuple of template file name (i.e. `coltrane/content.html`) and context
            dictionary.
        """

        (html, metadata) = self.get_html_and_markdown(slug)
        context = {}

        # Start with any metadata from the markdown frontmatter
        context.update(metadata)

        # Add JSON data to the context
        data = get_data()
        context["data"] = data

        if request:
            context["request"] = request

        # Add rendered content to the context
        content = self.render_html_with_django(html, context, request)

        context["content"] = mark_safe(content)
        template = context["template"]

        return (template, context)

    @classmethod
    def instance(cls) -> Union["Markdown2MarkdownRenderer", "MistuneMarkdownRenderer"]:
        if cls._instance is None:
            markdown_renderer = get_markdown_renderer()

            if markdown_renderer == "markdown2":
                cls._instance = Markdown2MarkdownRenderer()
            elif markdown_renderer == "mistune":
                cls._instance = MistuneMarkdownRenderer()
            else:
                raise AssertionError("Invalid markdown renderer")

        return cls._instance


class Markdown2MarkdownRenderer(MarkdownRenderer):
    def _parse_and_update_metadata(self, content: Markdown) -> dict:
        """
        Add new, parse and/or cast existing values to metadata.
        """

        metadata = content.metadata or {}

        if "publish_date" in metadata:
            metadata["publish_date"] = dateparser.parse(metadata["publish_date"])

        if "draft" in metadata:
            metadata["draft"] = metadata["draft"] == "true"

        metadata["now"] = now()

        if hasattr(content, "toc_html"):
            metadata["toc"] = None

            if content.toc_html:
                metadata["toc"] = mark_safe(content.toc_html)

        return metadata

    def render_markdown_text(self, text: str) -> Tuple[str, Dict]:
        text = self.pre_process_markdown(text)

        markdown_extras = get_markdown_extras()
        markdown_content = markdown(text=text, extras=markdown_extras)

        content = str(markdown_content)
        content = self.post_process_html(content)

        metadata = self._parse_and_update_metadata(markdown_content)

        return (content, metadata)


class MistuneMarkdownRenderer(MarkdownRenderer):
    try:
        from mistune.renderers.html import HTMLRenderer
    except ImportError:
        HTMLRenderer = object

    class CustomHTMLRenderer(HTMLRenderer):
        def _color_with_pygments(self, codeblock, lexer, **formatter_opts):
            import pygments
            from pygments.formatters import HtmlFormatter

            class HtmlCodeFormatter(HtmlFormatter):
                def _wrap_code(self, inner):
                    """
                    A function for use in a Pygments Formatter which wraps in <code> tags.
                    """

                    yield 0, "<code>"
                    yield from inner
                    yield 0, "</code>"

                def _add_newline(self, inner):
                    # Add newlines around the inner contents so that _strict_tag_block_re matches the outer div.
                    yield 0, "\n"
                    yield from inner
                    yield 0, "\n"

                def wrap(self, source):
                    """
                    Return the source with a code, pre, and div.
                    """

                    return self._add_newline(self._wrap_pre(self._wrap_code(source)))

            formatter_opts.setdefault("cssclass", "codehilite")
            formatter = HtmlCodeFormatter(**formatter_opts)

            return pygments.highlight(codeblock, lexer, formatter)

        def block_code(self, code: str, info=None) -> str:
            import mistune
            from pygments.lexers import get_lexer_by_name
            from pygments.util import ClassNotFound

            language = ""

            if info is not None:
                info = mistune.renderers.html.safe_entity(info.strip())
                language = info.split(None, 1)[0]

                if language:
                    try:
                        lexer = get_lexer_by_name(language)

                        return self._color_with_pygments(code, lexer)
                    except ClassNotFound:
                        pass

            return f"<pre><code>{code}</code></pre>\n"

    def __init__(self):
        import mistune
        from mistune.directives import Admonition, FencedDirective

        plugins = [*get_mistune_plugins(), FencedDirective([Admonition()])]

        self.mistune_markdown = mistune.create_markdown(
            renderer=MistuneMarkdownRenderer.CustomHTMLRenderer(),
            plugins=plugins,
        )

    def _parse_and_update_metadata(self, post) -> Dict:
        """
        Add new, parse and/or cast existing values to metadata.

        `metadata["toc"]` gets generated in `_generate_toc`.
        """

        metadata = post.metadata

        if "draft" in metadata:
            if metadata["draft"] is True:
                pass
            elif metadata["draft"] == "1":
                metadata["draft"] = True
            else:
                metadata["draft"] = False

        metadata["now"] = now()

        return metadata

    def _generate_toc(self, content, metadata):
        """
        Update the content to add links to each header and add a `toc` key to
        `metadata` with HTML for a table of contents.
        """

        from django.utils.html import strip_tags
        from minestrone import HTML

        html = HTML(content)

        last_header_int = None
        nested_count = 0
        strings = []

        for el in html.query("*"):
            if el.name not in ("h1", "h2", "h3", "h4", "h5", "h6"):
                continue

            header_text_slug = slugify(strip_tags(el.text))
            el.id = header_text_slug

            header_int = int(el.name[1:])

            if nested_count == 0:
                # Add the initial header
                strings.append("<ul>")
                nested_count += 1
            elif last_header_int < header_int:
                # The header is a higher number than the last one
                strings.append("<ul>")
                nested_count += 1
            elif last_header_int == header_int:
                # The header is at the same level
                strings.append("</li>")
            elif last_header_int > header_int:
                # The header is at a lower level
                for idx in range(nested_count):
                    if nested_count == 1:
                        # Last level so finish with a `li`
                        strings.append("</li>")
                    elif idx == (last_header_int - header_int):
                        # The current loop is equal to the difference
                        # between the last header and the current header
                        strings.append("</li>")
                    else:
                        # Skip down a level
                        strings.append("</li></ul>")

                    nested_count -= 1

                    if idx == (last_header_int - header_int):
                        # Break out of the loop because this iteration has gotten to the
                        # correct level
                        break

                nested_count += 1

            strings.append(f'<li><a href="#{header_text_slug}">{el.text}</a>')
            last_header_int = header_int

        # Close the correct number of `li` and `ul` tags at the end
        for _ in range(nested_count):
            strings.append("</li></ul>")

        toc_html = "".join(strings)

        metadata["toc"] = mark_safe(toc_html)
        content = str(html)

        return (content, metadata)

    def pre_process_markdown(self, text: str) -> str:
        text = super().pre_process_markdown(text)

        # Replace Django template variables in markdown with a marker for later because
        # mistune won't match markdown commands if there are empty strings
        text = re.sub(
            pattern=r"\({{\s*(\S+)\s*}}\)",
            repl=r"(DJANGO-TEMPLATE-VARIABLE-BEGIN-\g<1>-DJANGO-TEMPLATE-VARIABLE-END)",
            string=text,
            flags=re.RegexFlag.DOTALL,
        )

        # Get all matches for Django template tags for later adjustment
        pattern = r"\({%\s*(\S+)\s*(.*?)\s*%}\)"
        template_tag_matches = re.findall(pattern=pattern, string=text, flags=re.RegexFlag.DOTALL)

        # Replace Django template tags in markdown with a marker for later because
        # mistune won't match markdown commands if there are empty strings
        text = re.sub(
            pattern=pattern,
            repl=rf"(DJANGO-TEMPLATE-TAG-BEGIN-\g<1>{SPACE_REPLACEMENT}\g<2>-DJANGO-TEMPLATE-TAG-END)",
            string=text,
            flags=re.RegexFlag.DOTALL,
        )

        # Replace spaces between the Django template tag args/kwargs with something that
        # can be removed later
        for match in template_tag_matches:
            # Replace empty string with `SPACE_REPLACEMENT`
            # Replace double quote with a single quote
            template_tag_args = match[1].replace(" ", SPACE_REPLACEMENT).replace('"', "'")

            text = text.replace(match[1], template_tag_args)

        return text

    def post_process_html(self, html: str) -> str:
        html = super().post_process_html(html)

        # Replace the Django template language variable marker so that Django
        # variables will work for the next stage
        html = html.replace("DJANGO-TEMPLATE-VARIABLE-BEGIN-", "{{ ").replace("-DJANGO-TEMPLATE-VARIABLE-END", " }}")

        # Replace the Django template tag variable marker so that Django
        # template tags will work for the next stage
        html = html.replace("DJANGO-TEMPLATE-TAG-BEGIN-", "{% ").replace("-DJANGO-TEMPLATE-TAG-END", " %}")

        # Fix replacement string characters done in `pre_process_markdown`
        html = html.replace(SPACE_REPLACEMENT, " ")

        # Convert strings that were urlencoded by `mistune` back to their original form
        html = unquote(html)

        return html

    def render_markdown_text(self, text: str) -> Tuple[str, Dict]:
        import frontmatter

        frontmatter_post = frontmatter.loads(text)
        content = frontmatter_post.content

        content = self.pre_process_markdown(frontmatter_post.content)
        content = self.mistune_markdown(content)
        content = unescape(content)  # type: ignore
        content = self.post_process_html(content)

        metadata = self._parse_and_update_metadata(frontmatter_post)

        (content, metadata) = self._generate_toc(content, metadata)

        return (content, metadata)
