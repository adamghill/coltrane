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


def test_set_coltrane_setting_disable_wildcard_templates_true():
    expected = {"COLTRANE": {"DISABLE_WILDCARD_TEMPLATES": True}}

    settings = {"COLTRANE": {}}
    initialize_settings = {"COLTRANE_DISABLE_WILDCARD_TEMPLATES": True}
    setting_name = "DISABLE_WILDCARD_TEMPLATES"
    actual = _set_coltrane_setting(settings, initialize_settings, setting_name)

    assert expected == actual


def test_set_coltrane_setting_disable_wildcard_templates_true_string():
    expected = {"COLTRANE": {"DISABLE_WILDCARD_TEMPLATES": True}}

    settings = {"COLTRANE": {}}
    initialize_settings = {"COLTRANE_DISABLE_WILDCARD_TEMPLATES": "true"}
    setting_name = "DISABLE_WILDCARD_TEMPLATES"
    actual = _set_coltrane_setting(settings, initialize_settings, setting_name)

    assert expected == actual


def test_set_coltrane_setting_disable_wildcard_templates_not_true():
    expected = {"COLTRANE": {"DISABLE_WILDCARD_TEMPLATES": False}}

    settings = {"COLTRANE": {}}
    initialize_settings = {"COLTRANE_DISABLE_WILDCARD_TEMPLATES": 1}
    setting_name = "DISABLE_WILDCARD_TEMPLATES"
    actual = _set_coltrane_setting(settings, initialize_settings, setting_name)

    assert expected == actual


def test_set_coltrane_setting_is_secure_true():
    expected = {"COLTRANE": {"IS_SECURE": True}}

    settings = {"COLTRANE": {}}
    initialize_settings = {"COLTRANE_IS_SECURE": True}
    setting_name = "IS_SECURE"
    actual = _set_coltrane_setting(settings, initialize_settings, setting_name)

    assert expected == actual


def test_set_coltrane_setting_is_secure_true_string():
    expected = {"COLTRANE": {"IS_SECURE": True}}

    settings = {"COLTRANE": {}}
    initialize_settings = {"COLTRANE_IS_SECURE": "true"}
    setting_name = "IS_SECURE"
    actual = _set_coltrane_setting(settings, initialize_settings, setting_name)

    assert expected == actual


def test_set_coltrane_setting_is_secure_not_true():
    expected = {"COLTRANE": {"IS_SECURE": False}}

    settings = {"COLTRANE": {}}
    initialize_settings = {"COLTRANE_IS_SECURE": 1}
    setting_name = "IS_SECURE"
    actual = _set_coltrane_setting(settings, initialize_settings, setting_name)

    assert expected == actual
