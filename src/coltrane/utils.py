import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime
from functools import wraps

import dateparser
from django.utils.timezone import get_current_timezone, is_naive, make_aware

logger = logging.getLogger(__name__)


def dict_merge(
    source: dict,
    destination: dict,
    destination_overrides_source=False,  # noqa: FBT002
    path: list[str] | None = None,
) -> dict:
    """
    Deep merge two dictionaries.

    Shamelessly swiped from https://stackoverflow.com/a/7205107.
    """

    if path is None:
        path = []

    for key, value in destination.items():
        if key in source:
            if isinstance(source[key], dict) and isinstance(value, dict):
                dict_merge(
                    source=source[key],
                    destination=value,
                    destination_overrides_source=destination_overrides_source,
                    path=[*path, str(key)],
                )
            elif source[key] == value:
                pass  # same leaf value
            elif destination_overrides_source:
                source[key] = value
            else:
                msg = "Conflict at {}".format(".".join([*path, str(key)]))
                raise Exception(msg)
        else:
            source[key] = value

    return source


def convert_to_datetime(obj: str | int | datetime | date) -> datetime:
    """Convert different objects that could be a datetime into a datetime."""

    dt: datetime

    if isinstance(obj, datetime):
        dt = obj
    elif isinstance(obj, date):
        dt = datetime.combine(obj, datetime.min.time())
    elif isinstance(obj, str):
        dt = dateparser.parse(obj)  # type: ignore
    elif isinstance(obj, int):
        dt = datetime.fromtimestamp(obj)  # noqa: DTZ006
    else:
        raise TypeError(f"Unknown type for obj: {type(obj)!s}")

    if dt and is_naive(dt):
        dt = make_aware(dt, get_current_timezone())

    return dt


def threadpool(func):
    """
    A decorator to convert a regular function so that it gets run in another thread.

    ```python
    # does not block, returns Future object
    future = some_long_running_process()

    # this blocks, waiting for the result
    result = future.result()
    ```

    More details: https://stackoverflow.com/a/14331755
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        return ThreadPoolExecutor().submit(func, *args, **kwargs)

    return wrap
