import json
from hashlib import md5
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from django.core.management import call_command


def _call_build_command(*args, **kwargs) -> str:
    stdout = StringIO()
    stderr = StringIO()

    call_command(
        "build",
        *args,
        stdout=stdout,
        stderr=stderr,
        **kwargs,
    )

    assert not stderr.getvalue()

    return stdout.getvalue()


def _reset_settings(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.STATIC_ROOT = tmp_path / "output" / "static"


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_compress")
@patch("coltrane.management.commands.build.Command._call_collectstatic")
def test_build_command(_call_collectstatic, _call_compress, settings, tmp_path):
    _reset_settings(settings, tmp_path)

    # Create content file
    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text("# test 1")

    assert not (tmp_path / "output.json").exists()

    _call_build_command()

    _call_collectstatic.assert_called_once()
    _call_compress.assert_called_once()

    assert (tmp_path / "output").exists()
    assert (tmp_path / "output" / "test-1" / "index.html").exists()
    assert (tmp_path / "output.json").exists()


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_compress")
@patch("coltrane.management.commands.build.Command._call_collectstatic")
def test_build_command_index_md(_call_collectstatic, _call_compress, settings, tmp_path):
    _reset_settings(settings, tmp_path)

    # Create content file
    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "index.md").write_text("# index")

    assert not (tmp_path / "output.json").exists()

    _call_build_command()

    _call_collectstatic.assert_called_once()
    _call_compress.assert_called_once()

    assert (tmp_path / "output").exists()
    assert (tmp_path / "output" / "index.html").exists()
    assert (tmp_path / "output.json").exists()


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_compress")
@patch("coltrane.management.commands.build.Command._call_collectstatic")
def test_build_command_directory_index_md(_call_collectstatic, _call_compress, settings, tmp_path):
    _reset_settings(settings, tmp_path)

    # Create content file
    (tmp_path / "content").mkdir()
    (tmp_path / "content/dir").mkdir()
    (tmp_path / "content/dir/index.md").write_text("# dir")

    assert not (tmp_path / "output.json").exists()

    _call_build_command()

    _call_collectstatic.assert_called_once()
    _call_compress.assert_called_once()

    assert (tmp_path / "output").exists()
    assert (tmp_path / "output/dir").exists()
    assert (tmp_path / "output/dir/index.html").exists()
    assert (tmp_path / "output.json").exists()


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
def test_build_command_updates_output_manifest(settings, tmp_path):
    _reset_settings(settings, tmp_path)

    # Create output.json
    (tmp_path / "output.json").write_text("{}")

    # Create content directory
    (tmp_path / "content").mkdir()
    markdown_file = tmp_path / "content" / "test-1.md"
    markdown_file.write_text("# test 1")

    _call_build_command()

    assert (tmp_path / "output").exists()
    assert (tmp_path / "output" / "test-1" / "index.html").exists()

    mtime = markdown_file.stat().st_mtime
    file_hash = md5(markdown_file.read_bytes()).hexdigest()  # noqa: S324
    expected = '{"test-1.md": {"mtime": ' + str(mtime) + ', "md5": "' + file_hash + '"}}'
    actual = (tmp_path / "output.json").read_text()

    assert actual == expected


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
def test_build_command_force(settings, tmp_path):
    _reset_settings(settings, tmp_path)

    # Create content directory
    (tmp_path / "content").mkdir()

    stdout = _call_build_command("--force")

    assert "Force update because " in stdout


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
def test_build_command_staticfiles_force(settings, tmp_path):
    _reset_settings(settings, tmp_path)

    # Create content directory
    (tmp_path / "content").mkdir()

    # Create staticfiles.json
    (tmp_path / "output").mkdir()
    (tmp_path / "output" / "static").mkdir()
    (tmp_path / "output" / "static" / "staticfiles.json").write_text("{}")

    # Fake staticfiles.json metadata
    (tmp_path / "output.json").write_text(
        json.dumps(
            {
                "staticfiles.json": {"mtime": -1, "md5": "not-a-hash"},
            }
        )
    )

    stdout = _call_build_command()

    assert "Force update because static file(s) updated" in stdout
    assert (tmp_path / "output.json").exists()
