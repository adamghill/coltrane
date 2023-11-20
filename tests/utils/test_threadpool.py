from coltrane.utils import threadpool


def test_threadpool():
    @threadpool
    def _():
        return 1

    actual = _().result()
    assert actual == 1
