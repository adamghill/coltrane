import json
import logging
from typing import Dict

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
