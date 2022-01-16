import json
from dataclasses import dataclass
from hashlib import md5 as md5_hash
from pathlib import Path
from typing import Dict, Optional

from django.core.management.base import OutputWrapper
from django.template.loader import render_to_string
from django.utils.html import mark_safe  # type: ignore

from coltrane.config.paths import get_staticfiles_json
from coltrane.renderer import render_markdown


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
    def slug(self):
        """
        The name minus the extension. Not exactly a slug because it could contain a
        forward slash for directories.
        """

        return self.name.replace(".md", "")

    @property
    def name(self):
        """
        The name of the markdown file. Does not contain the whole path, it would contain
        everything after the `content` directory. Does contain the extension.

        For example: the `name` of `/tmp/new-site/content/2022/new-file.md`
            would be `2022/new-file.md`.
        """

        return self._name

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

    def render_html(self):
        """
        Renders the markdown file into HTML.
        """

        (template, context) = render_markdown(self.slug)
        rendered_html = render_to_string(template, context)

        return rendered_html

    @staticmethod
    def create(path: Path) -> "ManifestItem":
        """
        Initializes a new `ManifestItem` from a `Path`.
        """

        name = ManifestItem.get_name(path)
        mtime = path.stat().st_mtime
        md5 = md5_hash(path.read_bytes()).hexdigest()

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

            self._data[key] = ManifestItem(
                name=key, mtime=values.get("mtime"), md5=values.get("md5")
            )

    def __iter__(self):
        return iter(self._data.values())


@dataclass
class Manifest:
    """
    Represents a manifest file (output.json) which stores data for each markdown file
    that was output in the last build.
    """

    _manifest_file: Path
    _out: Optional[OutputWrapper]
    _items: ManifestItems
    _static_files_manifest_changed: bool = False
    _is_dirty: bool = False

    def __init__(
        self,
        manifest_file: Path,
        out: OutputWrapper = None,
    ):
        self._manifest_file = manifest_file
        self._out = out
        self._items = ManifestItems()

        if self._manifest_file.exists():
            self._items.load(manifest_file=manifest_file)

            if self._out:
                self._out.write("- Load manifest")

        staticfiles_manifest = get_staticfiles_json()

        if staticfiles_manifest.exists():
            if staticfiles_manifest_item := self.get(staticfiles_manifest):
                staticfiles_manifest_md5 = md5_hash(
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
