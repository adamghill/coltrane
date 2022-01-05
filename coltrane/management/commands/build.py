from django.conf import settings
from django.core.management.base import BaseCommand

from coltrane.manifest import Manifest, ManifestItem
from coltrane.retriever import get_content


class Command(BaseCommand):
    help = "Build all static HTML files and put them into a directory named output."

    def handle(self, *args, **options):
        output_dir = settings.BASE_DIR / "output"
        output_dir.mkdir(exist_ok=True)

        self.stdout.write(
            self.style.SUCCESS(
                f"Start to generate HTML and store in the '{output_dir}' directory..."
            )
        )

        content_paths = get_content()
        manifest = Manifest(
            manifest_file=settings.BASE_DIR / "output.json", out=self.stdout
        )

        self.stdout.write()

        for markdown_file in content_paths:
            item = ManifestItem.create(markdown_file)
            existing_item = manifest.get(markdown_file)

            if existing_item:
                skip_message = ""

                if item.mtime == existing_item.mtime:
                    skip_message = f"Skip generating {item.name} because not modified"
                elif item.md5 == existing_item.md5:
                    skip_message = (
                        f"Skip generating {item.name} because content not changed"
                    )

                    # Update item in manifest to get newest mtime
                    manifest.add(markdown_file)

                if skip_message:
                    self.stdout.write(self.style.WARNING(skip_message))
                    continue

            rendered_html = item.render_html()

            (output_dir / item.slug).mkdir(exist_ok=True)
            generated_file = output_dir / item.slug / "index.html"

            action = "Create"

            if generated_file.exists():
                action = "Update"

            generated_file.write_text(rendered_html)
            manifest.add(markdown_file)

            generated_file_name = f"{item.slug}/index.html"
            self.stdout.write(self.style.SUCCESS(f"{action} {generated_file_name}"))

        # TOOD: Handle files in output.json that weren't found in content (--clean option?)

        self.stdout.write()

        if manifest.is_dirty:
            self.stdout.write("Update output.json manifest...")
            manifest.write_data()

        self.stdout.write(self.style.SUCCESS("Finished generating HTML!"))
