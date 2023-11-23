# Environment

For local web development `coltrane` uses an `.env` file in the base directory for potentially sensitive settings. When deployed to production, those settings would be retrieved from environment variables (following the [12-factor app](https://12factor.net/config) method).

## Example `.env` file

```shell
DEBUG=True
INTERNAL_IPS=127.0.0.1
ALLOWED_HOSTS=example.com
COLTRANE_SITE_URL=https://example.com
SECRET_KEY=this-would-be-lots-of-random-characters
```

## Keys

### DEBUG

Whether the server is in debug mode or not. Error tracebacks, context, and sensitive information is displayed on the error page when this is set to `True`, so it should always be set to `False` when the app is deployed to production. Defaults to `True` for local development purposes.

### INTERNAL_IPS

Used to determine if the current request is internal or not. Must be set for the `debug` template variable to be populated (more information in the [Django documentation](https://docs.djangoproject.com/en/stable/ref/settings/#internal-ips)). Defaults to `127.0.0.1`. If more than one IP is required, separate them by commas.

```shell
INTERNAL_IPS=127.0.0.1,localhost,192.168.0.1
```

### SECRET_KEY

A random string of letters, numbers, and characters. (More information in the [Django documentation](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-SECRET_KEY). Generated automatically when the `.env` file is created. Required.

### ALLOWED_HOSTS

The acceptable host or domain names when the site is deployed to production. Must be set when `DEBUG` is set to `False`. Defaults to `""`. If more than one host name is required, separate them by commas.

```shell
ALLOWED_HOSTS=coltrane.com
```

### COLTRANE_SITE_URL

The hosting domain's scheme and domain. Required.

```shell
COLTRANE_SITE_URL=https://coltrane.com
```

### COLTRANE_TITLE

The title of the website. Required for generating `rss.xml`.

```shell
COLTRANE_TITLE=Coltrane
```

### COLTRANE_DESCRIPTION

The description of the website. Required for generating `rss.xml`.

```shell
COLTRANE_DESCRIPTION=A simple content site framework that harnesses the power of Django without the hassle.
```

### CACHE

The type of cache to use for `coltrane`. Acceptable options are: [`dummy`](https://docs.djangoproject.com/en/stable/topics/cache/#dummy-caching-for-development), [`memory`](https://docs.djangoproject.com/en/stable/topics/cache/#local-memory-caching), [`filesystem`](https://docs.djangoproject.com/en/stable/topics/cache/#filesystem-caching), [`memcache`](https://docs.djangoproject.com/en/stable/topics/cache/#memcached), or [`redis`](https://docs.djangoproject.com/en/stable/topics/cache/#redis). The default is `dummy`.

```{note}
`filesystem`, `memcache`, and `redis` options require `CACHE_LOCATION` to also be set.
```

### CACHE_LOCATION

The location of the cache. Required for `filesystem`, `memcache`, and `redis` cache options. The `filesystem` cache requires an absolute path. The `memcache` and `redis` cache options include multiple cache servers in a commma-delimited list.

### CONTENT_DIRECTORY

The directory that should be used for `markdown` content. Relative to the base directory. Defaults to "content".

### DATA_DIRECTORY

The directory that should be used for data. Relative to the base directory. Defaults to "data".
