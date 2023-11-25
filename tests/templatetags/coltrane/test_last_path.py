from coltrane.templatetags.coltrane_tags import last_path


class WSGIRequest:
    def __init__(self, path: str):
        self.path_info = path


def test_last_path_root():
    expected = ""

    context = {"request": WSGIRequest("/")}
    actual = last_path(context=context)

    assert expected == actual


def test_last_path_empty():
    expected = ""

    context = {"request": WSGIRequest("")}
    actual = last_path(context=context)

    assert expected == actual


def test_last_path_file():
    expected = "cool"

    context = {"request": WSGIRequest("/cool")}
    actual = last_path(context=context)

    assert expected == actual


def test_last_path_subdirectory():
    expected = "cool"

    context = {"request": WSGIRequest("/something/cool")}
    actual = last_path(context=context)

    assert expected == actual


def test_last_path_subdirectory_with_trailing_slash():
    expected = "something"

    context = {"request": WSGIRequest("/something/")}
    actual = last_path(context=context)

    assert expected == actual
