from coltrane.config import settings


class IsSecureMiddleware:
    """Overrides request.is_secure() to return `True` based on a setting.

    Only use if you're **always** serving with HTTPS.

    Based on https://noumenal.es/notes/til/django/csrf-trusted-origins/ and
    https://gist.github.com/carltongibson/648099cd34b2c0a18e948c917a5c48fd.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.is_secure() and settings.get_is_secure():
            # Override `request.is_secure`
            request.is_secure = lambda: True

        response = self.get_response(request)
        return response
