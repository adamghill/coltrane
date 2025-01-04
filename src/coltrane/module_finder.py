from importlib.util import find_spec


def is_module_available(module_name: str) -> bool:
    """
    Helper function to check if a module is available.

    Could be an installed package or an available module.
    """

    return find_spec(module_name) is not None


def is_whitenoise_installed() -> bool:
    """
    Helper function to check if `whitenoise` is installed.
    """

    return is_module_available("whitenoise")


def is_django_compressor_installed() -> bool:
    """
    Helper function to check if `django-compressor` is installed.
    """

    return is_module_available("compressor")


def is_dj_angles_installed() -> bool:
    """
    Helper function to check if `dj_angles` is installed.
    """

    return is_module_available("dj_angles")


def is_django_unicorn_installed() -> bool:
    """
    Helper function to check if `django_unicorn` is installed.
    """

    return is_module_available("django_unicorn")


def is_unicorn_module_available() -> bool:
    """
    Helper function to check if there is a `unicorn` app available.
    """

    return is_module_available("unicorn")
