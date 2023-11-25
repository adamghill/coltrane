from coltrane.templatetags.coltrane_tags import paths


class WSGIRequest:
    def __init__(self, path: str):
        self.path_info = path


def test_paths_root():
    expected = []

    context = {"request": WSGIRequest("/")}
    actual = paths(context=context)

    assert expected == actual


def test_paths_empty():
    expected = []

    context = {"request": WSGIRequest("")}
    actual = paths(context=context)

    assert expected == actual


def test_paths_file():
    expected = ["cool"]

    context = {"request": WSGIRequest("/cool")}
    actual = paths(context=context)

    assert expected == actual


def test_paths_subdirectory():
    expected = ["something", "cool"]

    context = {"request": WSGIRequest("/something/cool")}
    actual = paths(context=context)

    assert expected == actual


def test_paths_subdirectory_with_trailing_slash():
    expected = ["something"]

    context = {"request": WSGIRequest("/something/")}
    actual = paths(context=context)

    assert expected == actual
