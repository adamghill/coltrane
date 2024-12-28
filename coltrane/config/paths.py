from os import getcwd
from pathlib import Path
from typing import Iterable, Optional

from django.conf import settings

from coltrane.config.coltrane import Site
from coltrane.config.settings import get_content_directory as get_content_directory_setting
from coltrane.config.settings import get_data_directory as get_data_directory_setting
from coltrane.config.settings import get_extra_file_names


def get_base_directory(site: Optional[Site] = None) -> Path:
    """
    Get base directory from settings or return the default of the current directory.
    """

    base_dir = None

    if hasattr(settings, "BASE_DIR"):
        base_dir = Path(settings.BASE_DIR)
    else:
        base_dir = Path(getcwd())

    if site and site.is_custom:
        base_dir /= site.folder

    return base_dir


def get_site_directory(site: Site) -> Path:
    """
    Get site directory.
    """

    site_dir = get_base_directory()

    if site.is_custom:
        site_dir /= site.folder

    return site_dir


def get_data_directory(site: Site) -> Path:
    """
    Get the path of the JSON `data` directory.
    """

    return get_site_directory(site=site) / get_data_directory_setting()


def get_content_directory(site: Optional[Site] = None) -> Path:
    """
    Get the path of the markdown `content` directory.
    """

    if site:
        return get_site_directory(site=site) / get_content_directory_setting()

    return get_base_directory() / get_content_directory_setting()


def get_extra_file_paths() -> Iterable[Path]:
    for file_name in get_extra_file_names():
        file_path = get_file_path(file_name)

        if file_path.exists():
            yield file_path


def get_file_path(file_name: str, site: Optional[Site] = None) -> Path:
    """
    Get the path of a file in the content directory.
    """

    return get_content_directory(site=site) / file_name


def get_output_directory_name() -> str:
    """
    Gets the output directory name from settings if it is set. Defaults to "output".
    """

    output_directory_name = "output"

    try:
        output_directory_name = settings.COLTRANE["OUTPUT"]["PATH"]
    except (AttributeError, KeyError):
        pass

    return output_directory_name


def get_output_directory() -> Path:
    """
    Get the path that HTML files will be output to.
    """

    try:
        return Path(settings.COLTRANE["OUTPUT"]["DIRECTORY"])
    except (AttributeError, KeyError):
        pass

    return get_base_directory() / get_output_directory_name()


def get_output_json() -> Path:
    """
    Get the path of the JSON manifest `output.json` file.
    """

    return get_base_directory() / "output.json"


def get_staticfiles_json() -> Path:
    """
    Get the path of Django's `staticfiles.json` manifest file.
    """

    return Path(settings.STATIC_ROOT) / "staticfiles.json"


def get_output_static_directory() -> Path:
    """
    Get the path of Django's static path.
    """

    return Path(settings.STATIC_ROOT)


def get_redirects_json() -> Path:
    """
    Get the path of of the redirects.json file.
    """

    return get_base_directory() / "redirects.json"
