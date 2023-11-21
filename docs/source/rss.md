# RSS

`coltrane` automatically creates an `rss.xml` file containing all `markdown` content. It will be served from the `/rss.xml` URL or output into the `output` directory for static sites.

## Required setting

RSS requires an absolute URL so `coltrane` needs to know the domain for the site.

`COLTRANE_SITE_URL` needs to be set in the `.env` file.

## Django app configuration

When using `coltrane` as a `Django` app, RSS will [need to be configured](django-app/integration.md#rss).
