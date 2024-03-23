from pathlib import Path

import msgspec
import pytest

from coltrane.config.redirects import get_redirects


def test_get_redirects_url_url(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "redirects.json").write_text('{"/test-1": "/test-2"}')

    redirects = list(get_redirects())
    assert redirects

    actual = redirects[0]

    assert actual.from_url == "test-1"
    assert actual.to_url == "/test-2"
    assert actual.permanent is False


def test_get_redirects_url_dict(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "redirects.json").write_text('{"/test-3": {"url": "/test-4"}}')

    redirects = list(get_redirects())
    assert redirects

    actual = redirects[0]

    assert actual.from_url == "test-3"
    assert actual.to_url == "/test-4"
    assert actual.permanent is False


def test_get_redirects_url_dict_with_permanent(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "redirects.json").write_text('{"/test-5": {"url": "/test-6", "permanent": true}}')

    redirects = list(get_redirects())
    assert redirects

    actual = redirects[0]

    assert actual.from_url == "test-5"
    assert actual.to_url == "/test-6"
    assert actual.permanent is True


def test_get_redirects_url_dict_missing_url(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "redirects.json").write_text('{"/test-5": {}}')

    with pytest.raises(msgspec.ValidationError) as e:
        list(get_redirects())

    assert "Object missing required field `url`" in e.exconly()
