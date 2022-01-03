import pytest

from coltrane.utils import dict_merge


def test_dict_merge_source_into_destination():
    source = {"src": 1}
    destination = {"dest": 2}

    expected = {"src": 1, "dest": 2}
    actual = dict_merge(source, destination)

    assert actual == expected


def test_dict_merge_existing_key():
    source = {"test": 1}
    destination = {"test": 2}

    with pytest.raises(Exception) as e:
        dict_merge(source, destination)

    assert e.exconly() == "Exception: Conflict at test"


def test_dict_merge_override_existing_key():
    source = {"test": 1, "src": 3}
    destination = {"test": 2, "dest": 4}

    expected = {"test": 2, "src": 3, "dest": 4}
    actual = dict_merge(source, destination, destination_overrides_source=True)

    assert actual == expected


def test_dict_merge_recursive():
    source = {"src": {"test": {"more": 1}}}
    destination = {"dest": {"test": {"more": 2}}}

    expected = {"src": {"test": {"more": 1}}, "dest": {"test": {"more": 2}}}
    actual = dict_merge(source, destination, destination_overrides_source=True)

    assert actual == expected


def test_dict_merge_same_value():
    source = {"test": 1, "src": 3}
    destination = {"test": 1, "dest": 4}

    expected = {"test": 1, "src": 3, "dest": 4}
    actual = dict_merge(source, destination)

    assert actual == expected


def test_dict_merge_initial_path():
    source = {"test": 1, "src": 3}
    destination = {"test": 1, "dest": 4}

    expected = {"test": 1, "src": 3, "dest": 4}
    actual = dict_merge(source, destination, path=[])

    assert actual == expected
