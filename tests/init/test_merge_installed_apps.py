from coltrane import _merge_installed_apps


def test_merge_installed_apps_no_installed_apps_in_settings():
    expected = ["coltrane"]
    actual = _merge_installed_apps({})

    assert actual == expected


def test_merge_installed_apps_installed_apps_in_settings():
    expected = ["test", "coltrane"]
    actual = _merge_installed_apps({"INSTALLED_APPS": ["test"]})

    assert actual == expected
