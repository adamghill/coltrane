from coltrane import DEFAULT_INSTALLED_APPS, _merge_installed_apps


def test_merge_installed_apps_no_installed_apps_in_settings():
    expected = DEFAULT_INSTALLED_APPS
    actual = _merge_installed_apps({})

    assert actual == expected


def test_merge_installed_apps_installed_apps_in_settings():
    expected = [
        "test",
    ]
    expected.extend(DEFAULT_INSTALLED_APPS)
    actual = _merge_installed_apps({"INSTALLED_APPS": ["test"]})

    assert actual == expected
