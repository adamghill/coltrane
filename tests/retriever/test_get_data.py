from pathlib import Path
from unittest.mock import patch

from coltrane.retriever import get_data


@patch("warnings.warn")
def test_get_data_json_file_logs_warning(
    warn,
    settings,
    tmp_path: Path,
):
    settings.BASE_DIR = tmp_path

    (tmp_path / "data.json").write_text("{}")

    get_data()

    warn.assert_called_once()


def test_get_data_json_file_skip_data(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "data.json").write_text('{"test":1}')

    expected = {}
    actual = get_data()

    assert actual == expected


def test_get_data_directory(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "test.json").write_text('{"sample":1}')

    expected = {"test": {"sample": 1}}
    actual = get_data()

    assert actual == expected


def test_get_data_directory_invalid_json(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "test.json").write_text("")

    expected = {}
    actual = get_data()

    assert actual == expected


def test_get_data_directory_sub_directories(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "test.json").write_text('{"sample1":1}')
    (tmp_path / "data" / "another").mkdir()
    (tmp_path / "data" / "another" / "great.json").write_text('{"sample2":2}')
    (tmp_path / "data" / "another" / "more").mkdir()
    (tmp_path / "data" / "another" / "more" / "awesome.json").write_text('{"sample3":3}')

    expected = {
        "test": {"sample1": 1},
        "another": {"great": {"sample2": 2}, "more": {"awesome": {"sample3": 3}}},
    }
    actual = get_data()

    assert actual == expected


def test_get_data_directory_sub_directory_with_json(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "test.json").write_text('{"sample1":1}')
    (tmp_path / "data" / "another.json").mkdir()

    expected = {
        "test": {"sample1": 1},
    }
    actual = get_data()

    assert actual == expected


def test_get_data_directory_sub_directory_with_json_utf8(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "test.json").write_text('{"sample1": "spræ"}')
    (tmp_path / "data" / "another.json").mkdir()

    expected = {
        "test": {"sample1": "spræ"},
    }
    actual = get_data()

    assert actual == expected


def test_get_data_directory_sub_directory_with_json5(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.COLTRANE["DATA_JSON5"] = True

    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "test.json").write_text('{"sample1":1,}')
    (tmp_path / "data" / "another.json").mkdir()

    expected = {
        "test": {"sample1": 1},
    }
    actual = get_data()

    assert actual == expected

    del settings.COLTRANE["DATA_JSON5"]


def test_get_data_directory_sub_directory_with_json5_utf8(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.COLTRANE["DATA_JSON5"] = True

    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "test.json").write_text('{"sample1": "spræ",}')
    (tmp_path / "data" / "another.json").mkdir()

    expected = {
        "test": {"sample1": "spræ"},
    }
    actual = get_data()

    assert actual == expected

    del settings.COLTRANE["DATA_JSON5"]


def test_get_data_directory_with_non_json_file(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "test1.json").write_text('{"sample":1}')
    (tmp_path / "data" / "test2.txt").write_text('{"sample":2}')

    expected = {"test1": {"sample": 1}}
    actual = get_data()

    assert actual == expected
