from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand

from coltrane.config.paths import get_output_directory, get_output_json
from coltrane.manifest import Manifest, ManifestItem
from coltrane.retriever import get_content


class Command(BaseCommand):
    help = "Build all static HTML files and put them into a directory named output."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force building all files",
        )

    def handle(self, *args, **options):
        is_force = False

        if options["force"]:
            is_force = True

        output_directory = get_output_directory()
        output_directory.mkdir(exist_ok=True)

        content_paths = get_content()
        manifest = Manifest(manifest_file=get_output_json(), out=self.stdout)

        self.stdout.write()

        for markdown_file in content_paths:
            item = ManifestItem.create(markdown_file)
            existing_item = manifest.get(markdown_file)

            if existing_item and not is_force:
                skip_message = ""

                if item.mtime == existing_item.mtime:
                    skip_message = (
                        f"- Skip {item.name} because the modified date is not changed"
                    )
                elif item.md5 == existing_item.md5:
                    skip_message = (
                        f"- Skip {item.name} because the content is not changed"
                    )

                    # Update item in manifest to get newest mtime
                    manifest.add(markdown_file)

                if skip_message:
                    self.stdout.write(skip_message)
                    continue

            rendered_html = item.render_html()

            item_path = output_directory

            for path in item.slug.split("/"):
                if path:
                    item_path = item_path / path
                    item_path.mkdir(exist_ok=True)

            generated_file = item_path / "index.html"

            action = "- Create"

            if generated_file.exists():
                action = "- Update"

            generated_file.write_text(rendered_html)
            manifest.add(markdown_file)

            generated_file_name = f"{item.slug}/index.html"
            self.stdout.write(f"{action} {generated_file_name}")

        # TOOD: Handle files in output.json that weren't found in content (--clean option?)

        if manifest.is_dirty:
            self.stdout.write("- Update output.json manifest...")
            manifest.write_data()

        self.stdout.write()

        self.stdout.write(self.style.SUCCESS(f"Output HTML to: {output_directory}"))

        management.call_command(
            "collectstatic", interactive=False, clear=True, verbosity=0
        )

        self.stdout.write(
            self.style.SUCCESS(f"Copied static files to: {settings.STATIC_ROOT}")
        )
