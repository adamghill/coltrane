import json
from hashlib import md5
from io import StringIO
from unittest.mock import patch

from django.conf import settings
from django.core.management import call_command


def _call_command(*args, **kwargs) -> str:
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


def test_handle(tmp_path):
    settings.BASE_DIR = tmp_path

    # Create content file
    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text("# test 1")

    stdout = _call_command()

    assert (tmp_path / "output").exists()
    assert (tmp_path / "output" / "test-1" / "index.html").exists()

    assert stdout.startswith("Start to generate HTML and store in ")
    assert "Create output.json manifest..." in stdout
    assert stdout.endswith("Finished generating HTML!\n")


def test_handle_updates_output_manifest(tmp_path):
    settings.BASE_DIR = tmp_path

    # Create output.json
    (tmp_path / "output.json").write_text("{}")

    # Create content directory
    (tmp_path / "content").mkdir()
    markdown_file = tmp_path / "content" / "test-1.md"
    markdown_file.write_text("# test 1")

    stdout = _call_command()

    assert (tmp_path / "output").exists()
    assert (tmp_path / "output" / "test-1" / "index.html").exists()

    mtime = markdown_file.stat().st_mtime
    hash = md5(markdown_file.read_bytes()).hexdigest()
    expected = '{"test-1.md": {"mtime": ' + str(mtime) + ', "md5": "' + hash + '"}}'
    actual = (tmp_path / "output.json").read_text()

    assert actual == expected

    assert "Load output.json manifest..." in stdout


def test_handle_skip_update_mtime(tmp_path):
    settings.BASE_DIR = tmp_path

    # Create output.json
    (tmp_path / "output.json").write_text("{}")

    # Create content directory
    (tmp_path / "content").mkdir()
    markdown_file = tmp_path / "content" / "test-1.md"
    markdown_file.write_text("# test 1")

    # Fake a previous run with the correct mtime
    mtime = markdown_file.stat().st_mtime
    (tmp_path / "output.json").write_text(
        json.dumps({"test-1.md": {"mtime": mtime, "md5": "not-a-hash"}})
    )

    stdout = _call_command()

    assert "Load output.json manifest..." in stdout
    assert "Skip generating test-1.md because not modified" in stdout


def test_handle_skip_update_md5(tmp_path):
    settings.BASE_DIR = tmp_path

    # Create output.json
    (tmp_path / "output.json").write_text("{}")

    # Create content directory
    (tmp_path / "content").mkdir()
    markdown_file = tmp_path / "content" / "test-1.md"
    markdown_file.write_text("# test 1")

    # Fake a previous run with the correct md5
    hash = md5(markdown_file.read_bytes()).hexdigest()
    (tmp_path / "output.json").write_text(
        json.dumps({"test-1.md": {"mtime": -1, "md5": hash}})
    )

    stdout = _call_command()

    assert "Load output.json manifest..." in stdout
    assert "Skip generating test-1.md because content not changed" in stdout
