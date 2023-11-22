from coltrane import _set_coltrane_setting


def test_set_coltrane_setting_missing_coltrane_in_settings():
    expected = {"COLTRANE": {"TITLE": "test title"}}

    settings = {}
    initialize_settings = {"COLTRANE_TITLE": "test title"}
    setting_name = "TITLE"
    actual = _set_coltrane_setting(settings, initialize_settings, setting_name)

    assert expected == actual


def test_set_coltrane_setting():
    expected = {"COLTRANE": {"TITLE": "test title"}}

    settings = {"COLTRANE": {}}
    initialize_settings = {"COLTRANE_TITLE": "test title"}
    setting_name = "TITLE"
    actual = _set_coltrane_setting(settings, initialize_settings, setting_name)

    assert expected == actual


def test_set_coltrane_setting_extra_file_names():
    expected = {"COLTRANE": {"EXTRA_FILE_NAMES": ["robots.txt"]}}

    settings = {"COLTRANE": {}}
    initialize_settings = {"COLTRANE_EXTRA_FILE_NAMES": "robots.txt"}
    setting_name = "EXTRA_FILE_NAMES"
    actual = _set_coltrane_setting(settings, initialize_settings, setting_name)

    assert expected == actual
