import os
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import BaseFinder
from django.core.files.storage import FileSystemStorage
from django.utils._os import safe_join

from coltrane.config.settings import get_config

searched_locations = []


class ColtraneSiteFinder(BaseFinder):
    """
    A static files finder that uses the Coltrane sites to locate files.
    Based on `django.contrib.staticfiles.finders.FileSystemFinder`.
    """

    def __init__(self, *args, **kwargs):
        # List of locations with static files
        self.locations = []

        # Maps dir paths to an appropriate storage instance
        self.storages = {}

        config = get_config()

        if config.site_type == config.SiteType.SITES:
            for site in config.sites:
                folder = settings.BASE_DIR / site.folder / "static"
                prefix = settings.BASE_DIR / site.folder / "static"

                self.locations.append((prefix, folder))

                filesystem_storage = FileSystemStorage(location=folder)
                filesystem_storage.prefix = prefix

                self.storages[folder] = filesystem_storage

        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return []

    def find(self, path, find_all=False, **kwargs):
        """
        Look for files in the extra locations as defined in STATICFILES_DIRS.
        """

        if kwargs:
            find_all = self._check_deprecated_find_param(find_all=find_all, **kwargs)

        matches = []

        for prefix, root in self.locations:
            if root not in searched_locations:
                searched_locations.append(root)

            matched_path = self.find_location(root, path, prefix)

            if matched_path:
                if not find_all:
                    return matched_path

                matches.append(matched_path)

        return matches

    def find_location(self, root, path, prefix=None):
        """
        Find a requested static file in a location and return the found
        absolute path (or ``None`` if no match).
        """

        if prefix:
            prefix = f"{prefix}{os.sep}"

            if not path.startswith(prefix):
                return None

            path = path.removeprefix(prefix)

        path = safe_join(root, path)

        if os.path.exists(path):
            return path

    def list(self, ignore_patterns):
        """
        List all files in all locations.
        """

        for _, root in self.locations:
            # Skip nonexistent directories.
            if os.path.isdir(root):
                storage = self.storages[root]

                for path in utils.get_files(storage, ignore_patterns):
                    yield path, storage
