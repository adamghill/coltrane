from coltrane.templatetags.coltrane_tags import last_path


def test_last_path_root(request):
    expected = ""

    request.path = "/"
    context = {"request": request}
    actual = last_path(context=context)

    assert expected == actual


def test_last_path_empty(request):
    expected = ""

    request.path = ""
    context = {"request": request}
    actual = last_path(context=context)

    assert expected == actual


def test_last_path_file(request):
    expected = "cool"

    request.path = "/cool"
    context = {"request": request}
    actual = last_path(context=context)

    assert expected == actual


def test_last_path_subdirectory(request):
    expected = "cool"

    request.path = "/something/cool"
    context = {"request": request}
    actual = last_path(context=context)

    assert expected == actual


def test_last_path_subdirectory_with_trailing_slash(request):
    expected = "something"

    request.path = "/something/"
    context = {"request": request}
    actual = last_path(context=context)

    assert expected == actual
