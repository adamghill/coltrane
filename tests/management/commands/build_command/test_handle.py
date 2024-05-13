import json
from hashlib import md5
from unittest.mock import Mock, patch

import pytest

from coltrane.management.commands.build import Command
from coltrane.manifest import Manifest


@pytest.fixture
def build_command():
    cmd = Command()
    cmd.is_force = False

    return cmd


def _reset_settings(settings, tmp_path):
    settings.BASE_DIR = tmp_path
    settings.STATIC_ROOT = tmp_path / "output" / "static"


def create_markdown_file(tmp_path):
    (tmp_path / "content").mkdir()
    markdown_file = tmp_path / "content" / "test-1.md"
    markdown_file.write_text("# test 1")

    return markdown_file


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
def test_handle_force_false(settings, tmp_path, build_command):
    _reset_settings(settings, tmp_path)

    # Create content directory
    (tmp_path / "content").mkdir()

    build_command.handle(force=False)

    assert build_command.is_force is False


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
def test_handle_force_true(settings, tmp_path, build_command):
    _reset_settings(settings, tmp_path)

    # Create content directory
    (tmp_path / "content").mkdir()

    build_command.handle(force=True)

    assert build_command.is_force is True


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._load_manifest", spec=Manifest)
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
def test_handle_static_files_changed_is_force(_load_manifest, settings, tmp_path, build_command):
    _reset_settings(settings, tmp_path)

    # Create content directory
    (tmp_path / "content").mkdir()

    _load_manifest.return_value.static_files_manifest_changed = True

    build_command.handle(force=False)

    assert build_command.is_force is True


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
def test_handle_create(settings, tmp_path, build_command):
    _reset_settings(settings, tmp_path)

    create_markdown_file(tmp_path)

    build_command.handle(force=False)

    assert build_command.output_result_counts.create_count == 1
    assert build_command.output_result_counts.update_count == 0
    assert build_command.output_result_counts.skip_count == 0


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
def test_handle_update(settings, tmp_path, build_command):
    _reset_settings(settings, tmp_path)

    create_markdown_file(tmp_path)

    # Fake a previous run with the invalid metadata
    (tmp_path / "output.json").write_text(json.dumps({"test-1.md": {"mtime": -1, "md5": "not-a-hash"}}))

    build_command.handle(force=False)

    assert build_command.output_result_counts.create_count == 0
    assert build_command.output_result_counts.update_count == 1
    assert build_command.output_result_counts.skip_count == 0


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
def test_handle_skip_because_mtime(settings, tmp_path, build_command):
    _reset_settings(settings, tmp_path)

    markdown_file = create_markdown_file(tmp_path)

    # Create output.json
    (tmp_path / "output.json").write_text("{}")

    # Fake a previous run with the correct md5
    md5_hash = md5(markdown_file.read_bytes()).hexdigest()  # noqa: S324
    (tmp_path / "output.json").write_text(json.dumps({"test-1.md": {"mtime": -1, "md5": md5_hash}}))

    build_command.handle(force=False)

    assert build_command.output_result_counts.create_count == 0
    assert build_command.output_result_counts.update_count == 0
    assert build_command.output_result_counts.skip_count == 1


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
def test_handle_skip_because_md5(settings, tmp_path, build_command):
    _reset_settings(settings, tmp_path)

    markdown_file = create_markdown_file(tmp_path)

    # Create output.json
    (tmp_path / "output.json").write_text("{}")

    # Fake a previous run with the correct mtime
    mtime = markdown_file.stat().st_mtime
    (tmp_path / "output.json").write_text(json.dumps({"test-1.md": {"mtime": mtime, "md5": "not-a-hash"}}))

    build_command.handle(force=False)

    assert build_command.output_result_counts.create_count == 0
    assert build_command.output_result_counts.update_count == 0
    assert build_command.output_result_counts.skip_count == 1


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
def test_handle_threads(settings, tmp_path, build_command):
    _reset_settings(settings, tmp_path)

    # Create content directory
    (tmp_path / "content").mkdir()

    build_command.handle(threads=3)

    assert build_command.threads_count == 3


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
def test_handle_invalid_threads_count(settings, tmp_path, build_command):
    _reset_settings(settings, tmp_path)

    # Create content directory
    (tmp_path / "content").mkdir()

    build_command.handle(threads="asdf")

    assert build_command.threads_count == 2  # default number of threads


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
@patch("coltrane.management.commands.build.cpu_count")
def test_handle_cpu_count_exception(cpu_count, settings, tmp_path, build_command):
    cpu_count.side_effect = Exception()
    _reset_settings(settings, tmp_path)

    # Create content directory
    (tmp_path / "content").mkdir()

    build_command.handle()

    assert build_command.threads_count == 2  # default number of threads


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
def test_handle_template_error_exit_with_1(settings, tmp_path, build_command):
    _reset_settings(settings, tmp_path)

    # Force debug to be true to surface template error
    settings.DEBUG = True

    # Create content file
    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text("{{sadf}}")

    with pytest.raises(SystemExit) as err:
        build_command.handle()

    assert err.type == SystemExit
    assert err.value.code == 1


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
def test_handle_template_error_formatted(settings, tmp_path, build_command):
    _reset_settings(settings, tmp_path)

    # Force debug to be true to surface template error
    settings.DEBUG = True

    # Create content file
    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text("{{sadf}}")

    with pytest.raises(SystemExit):
        build_command.handle()

    assert len(build_command.errors) == 1
    assert "'sadf' does not exist in template context. Available top level variables:" in build_command.errors[0]


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
def test_handle_ignore_template_error(settings, tmp_path, build_command):
    _reset_settings(settings, tmp_path)

    # Force debug to be true to surface template error
    settings.DEBUG = True

    # Create content file
    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text("{{sadf}}")

    # Ignore the template error so exit isn't called
    build_command.handle(ignore=True)


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
@patch("coltrane.management.commands.build.Command._generate_sitemap")
def test_handle_generate_sitemap(
    _generate_sitemap,
    settings,
    tmp_path,
    build_command,
):
    _reset_settings(settings, tmp_path)

    create_markdown_file(tmp_path)

    build_command.handle(force=False)

    _generate_sitemap.assert_called_once()


@pytest.mark.slow
@patch("coltrane.management.commands.build.Command._call_collectstatic", Mock())
@patch("coltrane.management.commands.build.Command._call_compress", Mock())
@patch("coltrane.management.commands.build.Command._generate_rss")
def test_handle_generate_rss(
    _generate_rss,
    settings,
    tmp_path,
    build_command,
):
    _reset_settings(settings, tmp_path)

    create_markdown_file(tmp_path)

    build_command.handle(force=False)

    _generate_rss.assert_called_once()
