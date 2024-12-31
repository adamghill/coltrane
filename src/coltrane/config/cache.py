from dataclasses import dataclass

from django.core.cache import caches
from django.core.cache.backends.base import BaseCache

from coltrane.config.settings import get_coltrane_settings

AVAILABLE_CACHE_SETTINGS_KEYS = [
    "VIEW_CACHE",
    "DATA_CACHE",
]


@dataclass
class Cache:
    settings_key: str
    cache_key_namespace: str
    cache: BaseCache
    seconds: int
    is_enabled: bool = False

    def __init__(self, settings_key: str):
        self.settings_key = settings_key

        if self.settings_key not in AVAILABLE_CACHE_SETTINGS_KEYS:
            raise AssertionError("Invalid cache settings key")

        coltrane_settings = get_coltrane_settings()

        self.is_enabled = "SECONDS" in coltrane_settings.get(self.settings_key, {})

        if self.is_enabled:
            seconds = coltrane_settings[self.settings_key]["SECONDS"]

            if seconds is None:
                self.seconds = None
            else:
                self.seconds = int(seconds)

            self.cache_key_namespace = f"coltrane:{self.settings_key.lower()}:"

            cache_name = coltrane_settings[self.settings_key].get("CACHE_NAME", "default")
            self.cache = caches[cache_name]


@dataclass
class ViewCache(Cache):
    def __init__(self):
        super().__init__("VIEW_CACHE")


@dataclass
class DataCache(Cache):
    def __init__(self):
        super().__init__("DATA_CACHE")
