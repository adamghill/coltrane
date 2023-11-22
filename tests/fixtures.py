from os import environ

import pytest


@pytest.fixture
def env():
    # Store the original environment
    _original_environ = environ.copy()

    # Runs the test
    try:
        yield
    except:  # noqa: E722, S110
        pass
    finally:
        # Set the environment back to the original
        environ.clear()
        environ.update(_original_environ)
