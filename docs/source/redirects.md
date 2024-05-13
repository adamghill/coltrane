# Redirects

The `redirects.json` file can be used to redirect a user from a certain URL to another URL.

```{note}
Redirects are not supported when building a static site.
```

The `redirects.json` file is a dictionary where the key is a string of the URL that will get redirected _away_ from. 

The value is either:
- a string of the URL to temporarily redirect _to_, i.e. it redirects with a 302 status code
- a dictionary with a `url` and `permanent` keys; if `permanent` is set to `false` or is missing, the status code will be a 302; if it is set to `true`, the status code will be a 301

```json
{
    "/current-url": "/new-url",
    "/another-url": { "url": "/new-url", "permanent": false },
}
```
