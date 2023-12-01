from copy import deepcopy

from coltrane import DEFAULT_INSTALLED_APPS, _merge_installed_apps


def test_merge_installed_apps_no_installed_apps_in_settings():
    expected = DEFAULT_INSTALLED_APPS
    actual = _merge_installed_apps({}, deepcopy(DEFAULT_INSTALLED_APPS))

    assert actual == expected


def test_merge_installed_apps_installed_apps_in_settings():
    expected = [*deepcopy(DEFAULT_INSTALLED_APPS), "test"]

    django_settings = {"INSTALLED_APPS": ["test"]}
    actual = _merge_installed_apps(django_settings, deepcopy(DEFAULT_INSTALLED_APPS))

    assert actual == expected

    # Make sure that INSTALLED_APPS gets popped out of settings
    assert "INSTALLED_APPS" not in django_settings
