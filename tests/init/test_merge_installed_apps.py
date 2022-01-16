from copy import deepcopy

from coltrane import DEFAULT_INSTALLED_APPS, _merge_installed_apps


def test_merge_installed_apps_no_installed_apps_in_settings():
    expected = DEFAULT_INSTALLED_APPS
    actual = _merge_installed_apps({}, deepcopy(DEFAULT_INSTALLED_APPS))

    assert actual == expected


def test_merge_installed_apps_installed_apps_in_settings():
    expected = deepcopy(DEFAULT_INSTALLED_APPS) + [
        "test",
    ]
    actual = _merge_installed_apps(
        {"INSTALLED_APPS": ["test"]}, deepcopy(DEFAULT_INSTALLED_APPS)
    )

    assert actual == expected
