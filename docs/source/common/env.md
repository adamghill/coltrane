# Environment

For local web development `coltrane` uses an `.env` file in the base directory for potentially sensitive settings. When deployed to production, those settings would be retrieved from environment variables (following the [12-factor app](https://12factor.net/config) method).

## Example `.env` file

```shell
DEBUG=True
INTERNAL_IPS=127.0.0.1
ALLOWED_HOSTS=
COLTRANE_SITE=
SECRET_KEY=this-would-be-lots-of-random-characters
```

## Keys

### DEBUG

Whether the server is in debug mode or not. Traceback, context, and sensitve information is displayed on the error page when this is set to `True`, so it should always be set to `False` when the app is deployed to production. Defaults to `True` for local development purposes.

### INTERNAL_IPS

Used to determine if the current request is internal or not. Must be set for the `debug` template variable to be populated (more information in the [Django documentation](https://docs.djangoproject.com/en/stable/ref/settings/#internal-ips)). Defaults to `127.0.0.1`. If more than one IP is required, separate them by commas.

```shell
INTERNAL_IPS=127.0.0.1,localhost,192.168.0.1
```

### ALLOWED_HOSTS

The acceptable host or domain names when the site is deployed to production. Must be set when `DEBUG` is set to `False`. Defaults to `""`. If more than one host name is required, separate them by commas.

```shell
ALLOWED_HOSTS=coltrane.com
```

### COLTRANE_SITE

The hosting domain's scheme and domain.

```shell
COLTRANE_SITE=https://coltrane.com
```

### COLTRANE_TITLE

The title of the website. Used when generating `rss.xml`.

```shell
COLTRANE_TITLE=Coltrane
```

### COLTRANE_DESCRIPTION

The description of the website. Used when generating `rss.xml`.

```shell
COLTRANE_DESCRIPTION=A simple content site framework that harnesses the power of Django without the hassle.
```

### SECRET_KEY

A random string of letters, numbers, and characters. (More information in the [Django documentation](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-SECRET_KEY). Generated automatically when the `.env` file is created.
