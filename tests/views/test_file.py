import importlib
from pathlib import Path

import pytest
from django.test import override_settings


@pytest.mark.urls("coltrane.urls")
def test_file_with_data(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.DEBUG = False
    settings.COLTRANE["EXTRA_FILE_NAMES"] = ["robots.txt"]

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "robots.txt").write_text("# allow all")

    # Import module and reload it to get the right routes
    from coltrane import urls

    importlib.reload(urls)

    with override_settings(ROOT_URLCONF=urls):
        response = client.get("/robots.txt")

    assert response.status_code == 200


def test_file_with_extra_file_names_setting(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.DEBUG = False
    settings.COLTRANE["EXTRA_FILE_NAMES"] = [
        "robots2.txt",
    ]

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "robots2.txt").write_text("# allow all")

    # Import module and reload it to get the right routes
    from coltrane import urls

    importlib.reload(urls)

    with override_settings(ROOT_URLCONF=urls):
        response = client.get("/robots2.txt")

    assert response.status_code == 200


def test_file_not_exists(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.DEBUG = True
    settings.COLTRANE["EXTRA_FILE_NAMES"] = ["robots.txt"]

    # Import module and reload it to get the right routes
    from coltrane import urls

    importlib.reload(urls)

    with override_settings(ROOT_URLCONF=urls):
        response = client.get("/robots.txt")

    assert response.status_code == 404

    # This will be robots.txt because the views.file route includes the
    # whole file name in the exception
    assert "robots.txt cannot be found" in response.content.decode()


@pytest.mark.urls("coltrane.urls")
def test_route_not_exists(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.DEBUG = True
    settings.COLTRANE["EXTRA_FILE_NAMES"] = [
        "robots.txt",
    ]

    # Import module and reload it to get the right routes
    from coltrane import urls

    importlib.reload(urls)

    with override_settings(ROOT_URLCONF=urls):
        response = client.get("/robots1.txt")

    assert response.status_code == 404

    # This will be robots1 and not robots1.txt because the catch-all route for markdown
    # content only includes the "slug"
    assert "robots1 cannot be found" in response.content.decode()
