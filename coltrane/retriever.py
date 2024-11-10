import json
import logging
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Optional

from coltrane.config.cache import DataCache
from coltrane.config.paths import get_content_directory, get_data_directory
from coltrane.config.settings import get_data_json_5
from coltrane.utils import dict_merge

logger = logging.getLogger(__name__)


MARKDOWN_EXTENSION_LENGTH = 3


def _add_data_from_path(data, data_directory, path):
    if path.is_file():
        directory_without_base_and_file_name = (str(path)).replace(str(data_directory), "").replace(path.name, "")

        # TODO: Check that .json5/.json is an extension first
        file_name = path.name.replace(".json5", "").replace(".json", "")
        value = None

        if get_data_json_5():
            try:
                import pyjson5

                try:
                    value = pyjson5.decode_buffer(path.read_bytes(), wordlength=0)
                except pyjson5.Json5DecoderException:
                    logger.exception(f"Invalid JSON5: '{file_name}'")
            except ImportError:
                pass
        else:
            try:
                value = json.loads(path.read_bytes())
            except json.decoder.JSONDecodeError:
                logger.exception(f"Invalid JSON: '{file_name}'")

        if value:
            new_data = {file_name: value}

            # For each part of the path between BASE_DIR/data and the JSON file,
            # add a new level (i.e. key) in the data dictionary; for example:
            # base_dir/data/some/new/test/here.json with {"one": "two"} ==
            # {"some": {"new": {"test": {"here": {"one": "two"}}}}}
            for key in reversed(directory_without_base_and_file_name.split("/")):
                if key:
                    new_data = {key: new_data}

            data = dict_merge(data, new_data)


def get_data() -> Dict:
    """
    Get and merge data from any JSON files recursively found in the `data` directory.
    """

    data = {}
    data_cache = DataCache()
    cache_key = ""

    if data_cache.is_enabled:
        cache_key = f"{data_cache.cache_key_namespace}data"
        data = data_cache.cache.get(cache_key, {})

        if data:
            return data

    data_directory = get_data_directory()

    for path in data_directory.rglob("*.json5"):
        _add_data_from_path(data, data_directory, path)

    for path in data_directory.rglob("*.json"):
        _add_data_from_path(data, data_directory, path)

    if data_cache.is_enabled:
        data_cache.cache.set(cache_key, data, timeout=data_cache.seconds)

    return data


def get_content_paths(slug: Optional[str] = None) -> Iterable[Path]:
    """
    Yield `Path`s for all markdown content in the content directory.
    """

    directory = get_content_directory()

    if slug:
        directory = directory / slug

    if not directory.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory}")

    paths = directory.rglob("*.md")

    for path in paths:
        if path.is_file():
            yield path


@dataclass
class ContentItem:
    path: Path
    metadata: Dict
    relative_url: str
    html: str


def get_content_items(skip_draft: bool = True) -> Iterable[ContentItem]:  # noqa: FBT001, FBT002
    from coltrane.renderer import MarkdownRenderer

    paths = get_content_paths()
    _items = []

    content_directory = get_content_directory()
    content_directory_path_length = len(str(content_directory))

    for path in paths:
        (html, metadata) = MarkdownRenderer.instance().render_markdown_path(path)

        if skip_draft and metadata and "draft" in metadata and metadata["draft"] is True:
            continue

        path_str = str(path)
        relative_url = path_str[content_directory_path_length:-MARKDOWN_EXTENSION_LENGTH]

        if relative_url.endswith("/index"):
            relative_url = relative_url[:-6]

        content_item = ContentItem(path=path, metadata=metadata, html=html, relative_url=relative_url)
        _items.append(content_item)

    return _items
