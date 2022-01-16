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


@patch("coltrane.management.commands.build.Command.call_collectstatic")
def test_handle(call_collectstatic, tmp_path):
    settings.BASE_DIR = tmp_path

    # Create content file
    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text("# test 1")

    stdout = _call_command()

    call_collectstatic.assert_called_once()

    assert (tmp_path / "output").exists()
    assert (tmp_path / "output" / "test-1" / "index.html").exists()

    assert stdout.startswith("Start generating the static ")
    assert "Load manifest" not in stdout
    assert "Update manifest" in stdout
    assert "Static site output completed in" in stdout


@patch("coltrane.management.commands.build.Command.call_collectstatic")
def test_handle_updates_output_manifest(call_collectstatic, tmp_path):
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

    assert "Load manifest" in stdout


@patch("coltrane.management.commands.build.Command.call_collectstatic")
def test_handle_skip_update_mtime(call_collectstatic, tmp_path):
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

    assert "Load manifest" in stdout
    assert "Skip output/test-1.md because the modified date is not changed" in stdout


@patch("coltrane.management.commands.build.Command.call_collectstatic")
def test_handle_skip_update_md5(call_collectstatic, tmp_path):
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

    assert "Load manifest" in stdout
    assert "Skip output/test-1.md because the content is not changed" in stdout


@patch("coltrane.management.commands.build.Command.call_collectstatic")
def test_handle_no_skip_create_html(call_collectstatic, tmp_path):
    settings.BASE_DIR = tmp_path

    # Create output.json
    (tmp_path / "output.json").write_text("{}")

    # Create content directory
    (tmp_path / "content").mkdir()
    markdown_file = tmp_path / "content" / "test-1.md"
    markdown_file.write_text("# test 1")

    # Fake a previous run with the correct md5
    (tmp_path / "output.json").write_text(
        json.dumps({"test-1.md": {"mtime": -1, "md5": "not-a-hash"}})
    )

    stdout = _call_command()

    assert "Load manifest" in stdout
    assert "Create output/test-1/index.html" in stdout


@patch("coltrane.management.commands.build.Command.call_collectstatic")
def test_handle_no_skip_update_html(call_collectstatic, tmp_path):
    settings.BASE_DIR = tmp_path

    # Create output.json
    (tmp_path / "output.json").write_text("{}")

    # Create content directory
    (tmp_path / "content").mkdir()
    markdown_file = tmp_path / "content" / "test-1.md"
    markdown_file.write_text("# test 1")

    # Create output directory
    (tmp_path / "output").mkdir()
    (tmp_path / "output" / "test-1").mkdir()
    html_file = tmp_path / "output" / "test-1" / "index.html"
    html_file.write_text("<h1>test 1</h1>")

    # Fake a previous run with the correct md5
    (tmp_path / "output.json").write_text(
        json.dumps({"test-1.md": {"mtime": -1, "md5": "not-a-hash"}})
    )

    stdout = _call_command()

    assert "Load manifest" in stdout
    assert "Update output/test-1/index.html" in stdout


@patch("coltrane.management.commands.build.Command.call_collectstatic")
def test_handle_force(call_collectstatic, tmp_path):
    settings.BASE_DIR = tmp_path

    # Create output.json
    (tmp_path / "output.json").write_text("{}")

    # Create content directory
    (tmp_path / "content").mkdir()
    markdown_file = tmp_path / "content" / "test-1.md"
    markdown_file.write_text("# test 1")

    # Create output directory
    (tmp_path / "output").mkdir()
    (tmp_path / "output" / "test-1").mkdir()
    html_file = tmp_path / "output" / "test-1" / "index.html"
    html_file.write_text("<h1>test 1</h1>")

    # Fake a previous run with the correct md5
    (tmp_path / "output.json").write_text(
        json.dumps({"test-1.md": {"mtime": -1, "md5": "not-a-hash"}})
    )

    stdout = _call_command("--force")

    assert "Load manifest" in stdout
    assert "Force update because command line argument" in stdout
    assert "Update output/test-1/index.html" in stdout


@patch("coltrane.management.commands.build.Command.call_collectstatic")
def test_handle_staticfiles_force(call_collectstatic, tmp_path):
    settings.BASE_DIR = tmp_path
    settings.STATIC_ROOT = tmp_path / "output" / "static"

    # Create output.json
    # (tmp_path / "output.json").write_text("{}")

    # Create content directory
    (tmp_path / "content").mkdir()
    markdown_file = tmp_path / "content" / "test-1.md"
    markdown_file.write_text("# test 1")

    # Create output directory
    (tmp_path / "output").mkdir()
    (tmp_path / "output" / "test-1").mkdir()
    html_file = tmp_path / "output" / "test-1" / "index.html"
    html_file.write_text("<h1>test 1</h1>")

    # Create staticfiles.json
    (tmp_path / "output" / "static").mkdir()
    # (tmp_path / "output" / "test-1").mkdir()
    # html_file = tmp_path / "output" / "test-1" / "index.html"
    staticfiles_manifest = tmp_path / "output" / "static" / "staticfiles.json"
    staticfiles_manifest.write_text("{}")

    # Fake a previous run with the correct md5
    (tmp_path / "output.json").write_text(
        json.dumps(
            {
                "test-1.md": {"mtime": -1, "md5": "not-a-hash"},
                "staticfiles.json": {"mtime": -1, "md5": "not-a-hash"},
            }
        )
    )

    stdout = _call_command()

    assert "Load manifest" in stdout
    assert "Force update because static file(s) updated" in stdout
    assert "Update output/test-1/index.html" in stdout
