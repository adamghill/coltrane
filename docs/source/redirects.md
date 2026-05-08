# Redirects

Redirects can be configured in the `coltrane.toml` file to redirect users from one URL to another.

```{note}
Redirects are not supported when building a static site.
```

## Global Redirects

Global redirects are defined in the `[[redirects]]` sections of `coltrane.toml` and apply to all sites unless overridden by site-specific redirects.

```toml
[[redirects]]
from_url = "/current-url"
to_url = "/new-url"
permanent = false

[[redirects]]
from_url = "/another-url" 
to_url = "/new-url"
permanent = true
```

## Site-Specific Redirects

Site-specific redirects can be defined within each site's configuration and will override global redirects for that specific site.

```toml
[[sites]]
folder = "site1"
title = "Site 1"

[[sites.redirects]]
from_url = "/old-page"
to_url = "/new-page"
permanent = true
```

## Redirect Priority

1. Site-specific redirects (highest priority)
2. Global redirects from `coltrane.toml`

## Redirect Options

- `from_url`: The URL path to redirect from (with or without leading slash)
- `to_url`: The URL path to redirect to
- `permanent`: Set to `true` for 301 permanent redirects, `false` or omitted for 302 temporary redirects
