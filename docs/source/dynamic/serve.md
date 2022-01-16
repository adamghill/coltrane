# Serve

## Local development

`poetry run coltrane play` will serve the markdown files for local development.

```{warning}
`poetry run coltrane play` or Django's `runserver` management command is fine for local developement, but should never be used in production.
```

## Deployment

`coltrane` can be installed with deployment features for production by installing the `deploy` extras.

`poetry add coltrane-web -E deploy`

```{note}
If using `pip` you can do something like: `pip install coltrane-web[deploy]`.
```

### Required settings

[`DEBUG`](common/env#debug) should be `False` (more details in [Django docs](https://docs.djangoproject.com/en/stable/ref/settings/#debug)). [`ALLOWED_HOSTS`](common/env#allowed-hosts) must be set to the acceptable host or domain names (more details in [Django docs](https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts)).

```shell
DEBUG=False
ALLOWED_HOSTS=coltrane-web.com,www.coltrane-web.com
```

### Gunicorn

`gunicorn` is a production WSGI server. More information about it can be found at: https://gunicorn.org/.

Something like this could be used to start `gunicorn` with `coltrane`: `poetry run gunicorn -b localhost:8000 app:wsgi`.

### Whitenoise

`whitenoise` allows regular WSGI servers to serve static files without needing to move assets to S3 or another hosted file platform. More documentation is at: https://whitenoise.evans.io/.

### Recipe for Heroku

Heroku will run the `collectstatic` management command by default for Django projects, but this should be disabled for by setting the `DISABLE_COLLECTSTATIC` environment variable to `1`. Add the nginx buildpack from https://buildpack-registry.s3.amazonaws.com/buildpacks/heroku-community/nginx.tgz.

Then, add the following files so that `nginx` will serve the static files efficiently.

**`gunicorn.conf.py`**

```python
def when_ready(server):
    # touch app-initialized when ready
    open("/tmp/app-initialized", "w").close()


bind = "unix:///tmp/nginx.socket"
workers = 3
```

**`Procfile`**

```
web: python app.py collectstatic --noinput && bin/start-nginx gunicorn -c gunicorn.conf.py app:wsgi
```
