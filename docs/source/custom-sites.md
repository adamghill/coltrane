# Custom Sites

## Directory Structure

`coltrane` can serve multiple domains from a single project. To do this, create a `sites` directory and add a `coltrane.toml` file to it.

```bash
.
├── .gitignore
├── Dockerfile
├── README.md
├── pyproject.toml
└── sites
    ├── .env
    ├── .watchmanconfig
    ├── __init__.py
    ├── app.py
    ├── coltrane.toml
    ├── site-1
    │  ├── content
    │  ├── data
    │  ├── static
    │  └── templates
    ├── site-2
    │  ├── content
    │  ├── data
    │  ├── static
    │  └── templates
    └── gunicorn.conf.py
```

Then, create a directory for each site. For example, if you had 2 sites named `site-1` and `site-2`, the `site-1` site would be a folder named `sites/site-1`, and `site-2` would be in `sites/site-2`.

The directory structure for each site would be similar to a typical `coltrane` project.

## Configuration

The `coltrane.toml` file configures which folder will be used for a domain. For example, if you had 2 sites named `site-1` and `site-2`, you could configure `www.site-1.com` to serve serve content from `sites/site-1` and `www.site-2.com` to serve content from `sites/site-2`.

```toml
[[sites]]
folder = "site-1"
hosts = [
  "0.0.0.0:8020",
  "localhost:8020",
  "site-1.com"
  "www.site-1.com"
]

[[sites]]
folder = "site-2"
hosts = [
  "0.0.0.0:8021",
  "localhost:8021",
  "site-2.com"
  "www.site-2.com"
]
```

`coltrane` uses the `X-Forwarded-Host` and `X-Forwarded-Proto` headers to determine which site to serve content from. Based on the header, `coltrane` will server content from the appropriate site's folder.

```{note}
Do not forget to update `ALLOWED_HOSTS` for each site's domain.
```
