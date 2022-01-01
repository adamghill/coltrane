import logging
from typing import Dict

logger = logging.getLogger(__name__)


def dict_merge(source: Dict, destination: Dict, path: str = None) -> Dict:
    """
    Deep merge two dictionaries. Will overwrite existing dictionary keys if they exist in both.

    Shamelessly swiped from https://stackoverflow.com/a/7205107.
    """

    if path is None:
        path = []

    for key in destination:
        if key in source:
            if isinstance(source[key], dict) and isinstance(destination[key], dict):
                dict_merge(source[key], destination[key], path + [str(key)])
            elif source[key] == destination[key]:
                pass  # same leaf value
            else:
                raise Exception("Conflict at %s" % ".".join(path + [str(key)]))
        else:
            source[key] = destination[key]

    return source
