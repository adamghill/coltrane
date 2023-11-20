import json
from dataclasses import dataclass
from hashlib import md5 as md5_hash
from pathlib import Path
from typing import Dict, Optional

from django.template.loader import render_to_string

from coltrane.config.paths import get_output_directory, get_staticfiles_json
from coltrane.renderer import MarkdownRenderer, StaticRequest


@dataclass
class ManifestItem:
    """
    Stores information about a markdown file: the name, last modified time, and an MD5
    hash of the file contents.
    """

    _name: str
    _mtime: float
    _md5: str

    def __init__(self, name: str, mtime: float, md5: str):
        self._name = name
        self._mtime = mtime
        self._md5 = md5

    @property
    def slug(self) -> str:
        """
        The name minus the extension. Not exactly a slug because it could contain a
        forward slash for directories.
        """

        return self.name.replace(".md", "")

    @property
    def name(self) -> str:
        """
        The name of the markdown file. Does not contain the whole path, it would contain
        everything after the `content` directory. Does contain the extension.

        For example: the `name` of `/tmp/new-site/content/2022/new-file.md`
            would be `2022/new-file.md`.
        """

        return self._name

    @property
    def directory(self) -> str:
        """
        The directories before the file name.

        For example: the `path` of `/tmp/new-site/content/2022/new-file.md`
            would be `2022/`.
        """

        _directory = ""

        try:
            last_slash_idx = self.name.rindex("/")
            _directory = self.name[0:last_slash_idx]
        except ValueError:
            pass

        return f"/{_directory}"

    @property
    def mtime(self):
        """
        Last modified time of the file.
        """

        return self._mtime

    @property
    def md5(self):
        """
        MD5 hash of the file contents.
        """

        return self._md5

    @property
    def generated_file_path(self) -> Path:
        """
        The generated file path for the markdown file.
        """

        item_path = get_output_directory()

        for path in self.slug.split("/"):
            if path != "index":
                item_path = item_path / path
                item_path.mkdir(exist_ok=True)

        # index.md files be at the root as index.html
        if str(item_path).endswith("/index"):
            item_path = Path(str(item_path)[:-6])

        generated_file_path = item_path / "index.html"

        return generated_file_path

    @property
    def url_slug(self):
        url_slug = f"/{self.slug}"

        if url_slug.endswith("/index"):
            url_slug = url_slug[:-6]

        return url_slug

    def render_html(self):
        """
        Renders the markdown file into HTML.
        """

        # Mock an HttpRequest when generating the HTML for static sites
        request = StaticRequest(path=self.url_slug)

        (template, context) = MarkdownRenderer.instance().render_markdown(self.slug, request)
        rendered_html = render_to_string(template, context)

        return rendered_html

    @staticmethod
    def create(path: Path) -> "ManifestItem":
        """
        Initializes a new `ManifestItem` from a `Path`.
        """

        name = ManifestItem.get_name(path)
        mtime = path.stat().st_mtime
        md5 = md5_hash(path.read_bytes()).hexdigest()  # noqa: S324

        return ManifestItem(name=name, mtime=mtime, md5=md5)

    @staticmethod
    def get_name(path: Path) -> str:
        """
        Gets the `name` portion of the path, which is everything after the
        `content` directory.
        """

        name = ""

        if path.name == "staticfiles.json":
            return path.name

        # Assumes that there isn't a sub-folder called "content"
        for path_part in reversed(path.parts):
            if path_part == "content":
                break

            if path_part:
                if path_part == "/":
                    name = f"/{name}"
                elif name:
                    name = f"{path_part}/{name}"
                else:
                    name = path_part

        return name


@dataclass
class ManifestItems:
    """
    A store of all the markdown files in the manifest.
    """

    _data: Dict[str, ManifestItem]

    def __init__(self):
        self._data = {}

    def get(self, name: str) -> ManifestItem:
        """
        Gets the markdown file information by name.
        """

        return self._data[name]

    def add(self, manifest_item: ManifestItem) -> None:
        self._data[manifest_item.name] = manifest_item

    def load(self, manifest_file: Path) -> None:
        """
        Retrieve the current manifest file (typically output.json) and store the data.
        """

        initial_data = json.loads(manifest_file.read_bytes())

        for key in initial_data.keys():
            values = initial_data[key]

            self._data[key] = ManifestItem(name=key, mtime=values.get("mtime"), md5=values.get("md5"))

    def __iter__(self):
        return iter(self._data.values())


@dataclass
class Manifest:
    """
    Represents a manifest file (output.json) which stores data for each markdown file
    that was output in the last build.
    """

    _manifest_file: Path
    _items: ManifestItems
    _static_files_manifest_changed: bool = False
    _is_dirty: bool = False

    def __init__(self, manifest_file: Path):
        self._manifest_file = manifest_file
        self._items = ManifestItems()

        if self._manifest_file.exists():
            self._items.load(manifest_file=manifest_file)

        staticfiles_manifest = get_staticfiles_json()

        if staticfiles_manifest.exists():
            if staticfiles_manifest_item := self.get(staticfiles_manifest):
                staticfiles_manifest_md5 = md5_hash(  # noqa: S324
                    staticfiles_manifest.read_bytes()
                ).hexdigest()

                if staticfiles_manifest_item.md5 != staticfiles_manifest_md5:
                    self.add(staticfiles_manifest)
                    self._static_files_manifest_changed = True
            else:
                self.add(staticfiles_manifest)
                self._static_files_manifest_changed = True

    @property
    def is_dirty(self):
        """
        Whether the manifest file has been changed.
        """

        return self._is_dirty

    @property
    def static_files_manifest_changed(self):
        """
        Whether the staticfiles manifest has been changed.
        """

        return self._static_files_manifest_changed

    def add(self, path: Path) -> ManifestItem:
        """
        Adds a path (normally a markdown file, but could also be `staticfiles.json`) to
        the manifest. Also used to update an existing file in the manifest.
        """

        item = ManifestItem.create(path)
        self._items._data[item.name] = item
        self._is_dirty = True

        return item

    def get(self, markdown_file: Path) -> Optional[ManifestItem]:
        """
        Gets information about a markdown file from the manifest.
        """

        name = ManifestItem.get_name(markdown_file)

        try:
            return self._items.get(name)
        except KeyError:
            pass

        return None

    def write_data(self):
        """
        Writes the current manifest to the output file (typically output.json).
        """

        data = {}

        for item in self._items:
            data[item.name] = {"mtime": item.mtime, "md5": item.md5}

        self._manifest_file.write_text(json.dumps(data))
