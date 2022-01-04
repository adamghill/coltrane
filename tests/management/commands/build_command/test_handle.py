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

    with patch("coltrane.retriever.getcwd") as getcwd:
        getcwd.return_value = str(tmp_path)

        # Create content file
        (tmp_path / "content").mkdir()
        (tmp_path / "content" / "test-1.md").write_text("# test 1")

        stdout = _call_command(output=str((tmp_path / "output")))

        assert (tmp_path / "output").exists()
        assert (tmp_path / "output" / "test-1" / "index.html").exists()

    assert stdout.startswith("Starting to output HTML to ")
    assert stdout.endswith("Finished generating HTML!\n")
