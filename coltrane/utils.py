import logging
from typing import Dict, List


logger = logging.getLogger(__name__)


def dict_merge(
    source: Dict,
    destination: Dict,
    destination_overrides_source=False,
    path: List[str] = None,
) -> Dict:
    """
    Deep merge two dictionaries.

    Shamelessly swiped from https://stackoverflow.com/a/7205107.
    """

    if path is None:
        path = []

    for key in destination:
        if key in source:
            if isinstance(source[key], dict) and isinstance(destination[key], dict):
                dict_merge(
                    source=source[key],
                    destination=destination[key],
                    destination_overrides_source=destination_overrides_source,
                    path=path + [str(key)],
                )
            elif source[key] == destination[key]:
                pass  # same leaf value
            else:
                if destination_overrides_source:
                    source[key] = destination[key]
                else:
                    raise Exception("Conflict at %s" % ".".join(path + [str(key)]))
        else:
            source[key] = destination[key]

    return source
