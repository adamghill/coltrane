import json
import logging
from os import getcwd
from pathlib import Path
from typing import Dict, List

from django.conf import settings

from .utils import dict_merge


logger = logging.getLogger(__name__)


def get_data() -> Dict:
    """
    Get and merge data from `data.json` and any JSON files in the `data` directory.
    """

    data = {}

    try:
        with open(settings.BASE_DIR / "data.json", "r") as f:
            data = json.loads(f.read())
    except FileNotFoundError:
        logger.debug("Missing data.json file")

    try:
        for file in (settings.BASE_DIR / "data").iterdir():
            if file.name.endswith(".json"):
                file_name = file.name.replace(".json", "")
                data = dict_merge(data, {file_name: json.loads(file.read_text())})
    except FileNotFoundError:
        logger.debug("Missing data directory")

    return data


def get_content() -> List[Path]:
    """
    Get a list of `Path`s for all markdown content.
    """

    current_dir = Path(getcwd())
    paths = []

    def _get_markdown_file_paths(directory):
        if not directory.exists():
            raise FileNotFoundError(f"Directory does not exist: {directory}")

        for path in directory.rglob("*.md"):
            if path.is_dir():
                _get_markdown_file_paths(path)
            elif path.is_file:
                paths.append(path)

    _get_markdown_file_paths(current_dir / "content")

    return paths
