from coltrane.config.paths import get_output_static_directory


def test_static_root(settings):
    settings.STATIC_ROOT = "test-root"
    actual = get_output_static_directory()

    assert str(actual) == "test-root"
