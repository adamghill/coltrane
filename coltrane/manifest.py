import json
from dataclasses import dataclass
from hashlib import md5 as md5_hash
from pathlib import Path
from typing import Dict, Optional

from django.core.management.base import OutputWrapper
from django.template.loader import render_to_string
from django.utils.html import mark_safe  # type: ignore

from coltrane.renderer import render_markdown


@dataclass
class ManifestItem:
    _name: str
    _mtime: float
    _md5: str

    def __init__(self, name: str, mtime: float, md5: str):
        self._name = name
        self._mtime = mtime
        self._md5 = md5

    @property
    def slug(self):
        return self.name.replace(".md", "")

    @property
    def name(self):
        return self._name

    @property
    def mtime(self):
        return self._mtime

    @property
    def md5(self):
        return self._md5

    def render_html(self):
        (content, data) = render_markdown(self.slug)

        rendered_html = render_to_string(
            "coltrane/content.html", {"content": mark_safe(content), "data": data}
        )

        return rendered_html

    @staticmethod
    def create(path: Path) -> "ManifestItem":
        name = ManifestItem.get_name(path)
        mtime = path.stat().st_mtime
        md5 = md5_hash(path.read_bytes()).hexdigest()

        return ManifestItem(name=name, mtime=mtime, md5=md5)

    @staticmethod
    def get_name(path: Path) -> str:
        name = ""

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
    _data: Dict[str, ManifestItem]

    def __init__(self):
        self._data = {}

    def get(self, name: str) -> ManifestItem:
        return self._data[name]

    def load(self, manifest_file: Path) -> None:
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
    _manifest_file: Path
    _out: Optional[OutputWrapper]
    _items: ManifestItems
    _is_dirty: bool = False

    def __init__(self, manifest_file: Path, out: OutputWrapper = None):
        self._manifest_file = manifest_file
        self._out = out
        self._items = ManifestItems()

        if self._manifest_file.exists():
            if self._out:
                self._out.write("Load output.json manifest...")

            self._items.load(manifest_file=manifest_file)
        else:
            if self._out:
                self._out.write("Create output.json manifest...")

    @property
    def is_dirty(self):
        return self._is_dirty

    def add(self, markdown_file: Path) -> ManifestItem:
        item = ManifestItem.create(markdown_file)
        self._items._data[item.name] = item
        self._is_dirty = True

        return item

    def get(self, markdown_file: Path) -> Optional[ManifestItem]:
        name = ManifestItem.get_name(markdown_file)

        try:
            return self._items.get(name)
        except KeyError:
            pass

        return None

    def write_data(self):
        data = {}

        for item in self._items:
            data[item.name] = {"mtime": item.mtime, "md5": item.md5}

        self._manifest_file.write_text(json.dumps(data))
