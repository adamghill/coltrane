from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Build all static HTML files and put them into the output directory."

    def add_arguments(self, parser):
        parser.add_argument("output", type=str)

    def handle(self, *args, **options):
        output_path = "output"

        if "output" in options:
            output_path = options["output"]

        print(f"Output into {output_path}")

        raise CommandError("Not implemented yet")
