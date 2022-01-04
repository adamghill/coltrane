from typing import List

from django.core.management.base import BaseCommand, CommandError


def get_markdown_file_paths() -> List[str]:
    return []


class Command(BaseCommand):
    help = "Build all static HTML files and put them into the output directory."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            action="store_true",
            default="output",
            help="Directory to write HTML",
        )

    def handle(self, *args, **options):
        output_path = options["output"]

        self.stdout.write(f"Output HTML to: {output_path}")

        raise CommandError("Not implemented yet")
