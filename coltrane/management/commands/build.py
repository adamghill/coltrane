import concurrent.futures
import logging
import time
from functools import wraps
from io import StringIO
from multiprocessing import cpu_count
from pathlib import Path
from types import SimpleNamespace

from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand

from halo import Halo
from log_symbols.symbols import LogSymbols

from coltrane.config.paths import (
    get_base_directory,
    get_output_directory,
    get_output_json,
    get_output_static_directory,
)
from coltrane.manifest import Manifest, ManifestItem
from coltrane.retriever import get_content_paths


logger = logging.getLogger(__name__)


_DEFAULT_POOL = concurrent.futures.ThreadPoolExecutor()


def threadpool(f, executor=None):
    @wraps(f)
    def wrap(*args, **kwargs):
        return (executor or _DEFAULT_POOL).submit(f, *args, **kwargs)

    return wrap


class Command(BaseCommand):
    help = "Build all static HTML files and put them into a directory named output."

    is_force = False
    manifest = None
    output_result_counts = SimpleNamespace(create_count=0, update_count=0, skip_count=0)

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force building all files",
        )

    def _load_manifest(self) -> Manifest:
        return Manifest(manifest_file=get_output_json())

    @threadpool
    def _call_collectstatic(self) -> str:
        stdout = StringIO()
        stderr = StringIO()

        # Force DEBUG to always be `False` so that
        # whitenoise.storage.CompressedManifestStaticFilesStorage will use the static
        # assets with hashed failenames
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

        # Get relative output static directory
        output_static_directory = str(get_output_static_directory()).replace(
            str(get_base_directory()), ""
        )
        output_static_directory = f"{output_static_directory}/"[1:]

        # Get output from standard out and clean it up
        stdout.seek(0)
        collectstatic_stdout = stdout.read()
        collectstatic_stdout = collectstatic_stdout.replace(
            "'" + str(get_output_static_directory()) + "'", output_static_directory
        )[1:-2]
        collectstatic_stdout = collectstatic_stdout.replace("copied ", "")
        collectstatic_stdout = "Copy " + collectstatic_stdout

        # TOOD: Handle files in output.json that weren't
        # found in content? (--clean option?)

        return collectstatic_stdout

    def _output_markdown_file(self, markdown_file: Path) -> None:
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

            item.generated_file.write_text(rendered_html)
            self.manifest.add(markdown_file)

    def _success(self, text: str) -> None:
        self.stdout.write(LogSymbols.SUCCESS.value, ending=" ")
        self.stdout.write(text)

    def handle(self, *args, **options):
        self.is_force = False
        self.manifest = None
        self.output_result_counts.create_count = 0
        self.output_result_counts.update_count = 0
        self.output_result_counts.skip_count = 0

        start_time = time.time()

        self.stdout.write(self.style.WARNING("Start generating the static site...\n"))

        spinner = Halo(spinner="dots")

        collectstatic_future = self._call_collectstatic()

        output_directory = get_output_directory()
        spinner.start(f"Use '{output_directory}' as output directory")
        output_directory.mkdir(exist_ok=True)
        spinner.succeed()

        spinner.start("Load manifest")
        self.manifest = self._load_manifest()
        spinner.succeed()

        if options["force"]:
            self.is_force = True
            self._success("Force update because of command line argument")

        spinner.start("Collect static files")
        collectstatic_stdout = collectstatic_future.result()
        spinner.succeed(collectstatic_stdout)

        if not self.is_force and self.manifest.static_files_manifest_changed:
            # At least one static file has changed, so re-render all files because
            # we don't have granularity to know which static files are used in
            # particular markdown or template files
            self.is_force = True
            self._success("Force update because static file(s) updated")

        spinner.start("Output HTML files")

        single_thread_output = False

        try:
            if not single_thread_output:
                # TODO: Be able to pass in a number of threads to use
                threads_count = 2

                try:
                    threads_count = int(cpu_count() / 2) - 1
                except Exception:
                    pass

                with concurrent.futures.ThreadPoolExecutor(
                    max_workers=threads_count
                ) as executor:
                    logger.debug(f"Multithread with {threads_count} threads")
                    spinner.text = f"Output HTML files (use {threads_count} threads)"

                    for path in get_content_paths():
                        executor.submit(self._output_markdown_file, path)

                    # TODO: what happens if one thread throws an exception?
        except Exception as e:
            logger.debug(f"Fallback to single-thread because: {e}")
            single_thread_output = True

        if single_thread_output:
            spinner.text = "Output HTML files (single-threaded)"

            for content_path in get_content_paths():
                self._output_markdown_file(self.manifest, self.is_force, content_path)

        result_msg = f"Output HTML files (create: {self.output_result_counts.create_count}; update: {self.output_result_counts.update_count}; skip: {self.output_result_counts.skip_count})"

        spinner.succeed(result_msg)

        if self.manifest.is_dirty:
            spinner.start("Update manifest")
            self.manifest.write_data()
            spinner.succeed()

        self.stdout.write()

        elapsed_time = time.time() - start_time
        self.stdout.write(
            self.style.SUCCESS(f"Static site output completed in {elapsed_time:.4f}s")
        )
