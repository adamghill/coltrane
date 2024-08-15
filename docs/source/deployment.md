# Deployment

`coltrane` can be installed with deployment features for production by [installing the `deploy` extras](installation.md#extras).

```
coltrane[deploy]
```

## Required settings

- [`DEBUG`](env.md#debug) should be `False` (more details in [Django docs](https://docs.djangoproject.com/en/stable/ref/settings/#debug)).
- [`ALLOWED_HOSTS`](env.md#allowed_hosts) must be set to the acceptable host or domain names (more details in [Django docs](https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts)).

```shell
DEBUG=False
ALLOWED_HOSTS=coltrane.com,www.coltrane.com
```

## Gunicorn

[`gunicorn`](https://gunicorn.org) is a production `WSGI` server and is perfect for serving `coltrane` apps.

The following example shows how to run `gunicorn` in production.

```
gunicorn -b localhost:8000 app:wsgi
```

## Whitenoise

[`whitenoise`](https://whitenoise.evans.io/) allows regular `WSGI` servers to serve static files without needing to move assets to S3 or another hosted file platform. It will be configured automatically when `DEBUG` is set to `False`.

## Hosting

### Docker

A sample `Dockerfile` is created for new `Coltrane` projects. It can be used along with `gunicorn.conf.py` for any hosting platform that supports `Docker`.

### Heroku

#### Integrated

1. Heroku will run the `collectstatic` management command by default for Django projects, but this should be disabled by setting the `DISABLE_COLLECTSTATIC` environment variable to `1`. This can be done in the _Config Vars_ section of the app `Settings`.

2. Turn off debug functionality by adding another environment variable key named `DEBUG` and setting the value to `0`.

![image](img/heroku-config-vars.png)

3. Add the `nginx` buildpack from https://buildpack-registry.s3.amazonaws.com/buildpacks/heroku-community/nginx.tgz and make sure it is the last buildpack in your list.

![image](img/heroku-buildpacks.png)

4. Then, add the following files so that `nginx` will serve the static files efficiently.

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

### render.com

#### Static site

- Set the `PYTHON_VERSION` environment variable to the desired Python version (must be at least 3.8)

![Render.com Python version](img/render-python-version.png)

- Go to `settings` and use `pip install uv && uv install -r pyproject.toml --system && uv run coltrane build` for the `Build Command`

![Render.com build command](img/render-build-command.png)
