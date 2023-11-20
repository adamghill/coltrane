import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from io import StringIO
from multiprocessing import cpu_count
from pathlib import Path
from shutil import copy2
from types import SimpleNamespace
from typing import Dict, List, Optional

from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.core import management
from django.core.management.base import BaseCommand
from halo import Halo  # type: ignore
from log_symbols.symbols import LogSymbols  # type: ignore

from coltrane.config.paths import (
    get_base_directory,
    get_extra_file_paths,
    get_output_directory,
    get_output_json,
    get_output_static_directory,
)
from coltrane.feeds import ContentFeed
from coltrane.manifest import Manifest, ManifestItem
from coltrane.renderer import StaticRequest
from coltrane.retriever import get_content_paths
from coltrane.urls import sitemaps
from coltrane.utils import threadpool

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Build all static HTML files and put them into a directory named output."  # noqa: A003

    is_force = False
    threads_count = 2
    manifest = None
    output_result_counts = SimpleNamespace(create_count=0, update_count=0, skip_count=0)

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force building all files",
        )

        parser.add_argument(
            "--threads",
            action="store",
            help="Number of threads to use when generating static files",
        )

        parser.add_argument(
            "--output",
            action="store",
            help="Output directory",
        )

        parser.add_argument(
            "--ignore",
            action="store_true",
            help="Ignore errors",
        )

    def _load_manifest(self) -> Manifest:
        return Manifest(manifest_file=get_output_json())

    def _generate_sitemap(self) -> None:
        if not self.output_directory:
            raise AssertionError("Missing output directory")

        sitemap_response = sitemap(request=StaticRequest(path="/"), sitemaps=sitemaps)
        sitemap_xml = sitemap_response.render().content.decode()
        (self.output_directory / "sitemap.xml").write_text(sitemap_xml)

    def _generate_rss(self) -> None:
        if not self.output_directory:
            raise AssertionError("Missing output directory")

        content_feed = ContentFeed()
        feed = content_feed.get_feed(None, request=StaticRequest(path="/"))  # type: ignore
        rss_xml = feed.writeString("utf-8")

        (self.output_directory / "rss.xml").write_text(rss_xml)

    @threadpool
    def _call_collectstatic(self) -> str:
        stdout = StringIO()
        stderr = StringIO()

        # Force DEBUG to always be `False` so that
        # whitenoise.storage.CompressedManifestStaticFilesStorage will use the static
        # assets with hashed filenames
        settings.DEBUG = False

        # TODO: Option to remove static files before re-generating
        management.call_command(
            "collectstatic",
            interactive=False,
            verbosity=1,
            stdout=stdout,
            stderr=stderr,
        )

        stderr.seek(0)

        # Get output from standard out and clean it up
        stdout.seek(0)
        collectstatic_stdout = stdout.read()
        collectstatic_stdout = collectstatic_stdout.replace(f" copied to '{get_output_static_directory()!s}'", "")[1:-2]

        collectstatic_stdout = f"Copy {collectstatic_stdout}"

        # TODO: Handle files in output.json that weren't
        # found in content? (--clean option?)

        return collectstatic_stdout

    def _output_markdown_file(self, markdown_file: Path) -> None:
        if not self.manifest:
            raise AssertionError("Manifest must be loaded first")

        is_skipped = False

        item = ManifestItem.create(markdown_file)
        existing_item = self.manifest.get(markdown_file)

        if existing_item and not self.is_force:
            if item.mtime == existing_item.mtime:
                is_skipped = True
                self.output_result_counts.skip_count += 1
            elif item.md5 == existing_item.md5:
                # Update item in manifest to get newest mtime
                self.manifest.add(markdown_file)

                is_skipped = True
                self.output_result_counts.skip_count += 1

        if not is_skipped:
            if existing_item:
                self.output_result_counts.update_count += 1
            else:
                self.output_result_counts.create_count += 1

            rendered_html = item.render_html()

            item.generated_file_path.write_text(rendered_html)
            self.manifest.add(markdown_file)

    def _success(self, text: str, ending="\n") -> None:
        self.stdout.write(LogSymbols.SUCCESS.value, ending=" ")
        self.stdout.write(text, ending=ending)

    def _set_output_directory(self, options: Dict) -> None:
        if "output" in options and options["output"]:
            if not hasattr(settings, "COLTRANE"):
                settings.COLTRANE = {}

            if "OUTPUT" not in settings.COLTRANE:
                settings.COLTRANE["OUTPUT"] = {}

            settings.COLTRANE["OUTPUT"]["PATH"] = options["output"]

            # Override STATIC_ROOT if the output directory name is manually set
            try:
                settings.STATIC_ROOT = get_base_directory() / settings.COLTRANE["OUTPUT"]["PATH"] / "static"
            except KeyError:
                pass

            # Override STATIC_ROOT if the output directory is manually set
            try:
                settings.STATIC_ROOT = Path(settings.COLTRANE["OUTPUT"]["DIRECTORY"]) / "static"
            except KeyError:
                pass

    def handle(self, *args, **options):  # noqa: ARG002
        self.is_force: bool = False
        self.manifest: Optional[Manifest] = None
        self.output_result_counts.create_count = 0
        self.output_result_counts.update_count = 0
        self.output_result_counts.skip_count = 0
        self.output_directory: Optional[Path] = None
        self.errors: List[str] = []

        start_time = time.time()

        self.stdout.write(self.style.WARNING("Start generating the static site...\n"))

        spinner = Halo(spinner="dots")

        self._set_output_directory(options)

        collectstatic_future = self._call_collectstatic()

        self.output_directory = get_output_directory()
        self._success("Use output directory of ", ending="")
        self.stdout.write(self.style.WARNING(str(self.output_directory)))
        self.output_directory.mkdir(exist_ok=True)

        spinner.start("Load manifest")
        self.manifest = self._load_manifest()
        spinner.succeed()

        if "force" in options and options["force"] is True:
            self.is_force = True
            self._success("Force update because ", ending="")
            self.stdout.write(self.style.WARNING("--force"))

        spinner.start("Collect static files")
        collectstatic_stdout = collectstatic_future.result()
        spinner.succeed(collectstatic_stdout)

        spinner.start("Copy extra files")
        extra_file_count = 0
        for extra_file_path in get_extra_file_paths():
            copy2(extra_file_path, self.output_directory)
            extra_file_count += 1
        spinner.succeed(f"Copy {extra_file_count} extra files")

        if not self.is_force and self.manifest.static_files_manifest_changed:
            # At least one static file has changed, so re-render all files because
            # we don't have granularity to know which static files are used in
            # particular markdown or template files
            self.is_force = True
            self._success("Force update because static file(s) updated")

        if "threads" in options and options["threads"]:
            try:
                self.threads_count = int(options["threads"])
            except ValueError:
                pass
        else:
            try:
                self.threads_count = (cpu_count() // 2) - 1
            except Exception as ex:
                logger.exception(ex)

        spinner.start("Create HTML files")

        with ThreadPoolExecutor(max_workers=self.threads_count) as executor:
            logger.debug(f"Multithread with {self.threads_count} threads")
            pluralized_threads = "s" if self.threads_count > 1 else ""
            spinner.text = f"Create HTML files (use {self.threads_count} thread{pluralized_threads})"

            for path in get_content_paths():
                future = executor.submit(self._output_markdown_file, path)
                exception = future.exception()

                if exception:
                    error_detail = f"{exception.__class__.__name__}: {exception}"

                    if exception.__class__.__name__ == "FastDevVariableDoesNotExist":
                        error_detail = (
                            str(exception)
                            .replace("\n    ", ", ")
                            .replace(":\n, ", ": ")
                            .replace(
                                " does not exist in context.",
                                "' does not exist in template context.",
                            )
                        )[:-1]
                        error_detail = f"'{error_detail}"

                    error_message = f"Rendering {path} failed. {error_detail}"
                    self.errors.append(error_message)

        result_msg = f"Create {self.output_result_counts.create_count} HTML files, \
{self.output_result_counts.skip_count} unmodified, {self.output_result_counts.update_count} updated"

        spinner.succeed(result_msg)

        if self.manifest.is_dirty:
            spinner.start("Update sitemap.xml")
            self._generate_sitemap()
            spinner.succeed()

            spinner.start("Update rss.xml")
            self._generate_rss()
            spinner.succeed()

            spinner.start("Update output.json manifest")
            self.manifest.write_data()
            spinner.succeed()

        elapsed_time = time.time() - start_time

        for error_message in self.errors:
            spinner.fail(error_message)

        self.stdout.write()

        if self.errors:
            self.stderr.write(self.style.ERROR(f"Static site output completed with errors in {elapsed_time:.4f}s\n"))

            if "ignore" not in options or not options["ignore"]:
                # Call sys.exit explicitly instead of CommandError for nicer error output
                sys.exit(1)
        else:
            self.stdout.write(self.style.SUCCESS(f"Static site output completed in {elapsed_time:.4f}s"))
