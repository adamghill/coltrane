from pathlib import Path
from typing import List

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.utils.html import mark_safe  # type: ignore

from coltrane.renderer import render_markdown
from coltrane.retriever import get_content


class Command(BaseCommand):
    help = "Build all static HTML files and put them into the output directory."

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--output",
    #         action="store_true",
    #         default="output",
    #         help="Directory to write HTML",
    #     )

    def handle(self, *args, **options):
        # output_path = Path(options["output"])
        output_path = Path("output")

        self.stdout.write(f"Starting to output HTML to '{output_path}'...")

        content_paths = get_content()

        for path in content_paths:
            slug = path.name.replace(".md", "")
            (content, data) = render_markdown(slug)

            rendered_html = render_to_string(
                "coltrane/content.html", {"content": mark_safe(content), "data": data}
            )

            # TODO: Delete contents of output directory?

            output_path.mkdir(exist_ok=True)
            (output_path / slug).mkdir(exist_ok=True)
            (output_path / slug / "index.html").write_text(rendered_html)

            generated_file_name = (output_path / slug / "index.html").name

            self.stdout.write(f"Create {generated_file_name}")

        self.stdout.write()
        self.stdout.write(self.style.SUCCESS("Finished generating HTML!"))
