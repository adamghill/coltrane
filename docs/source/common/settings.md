# Settings

Settings specified in a `COLTRANE` dictionary.

```python
# default `coltrane` settings
COLTRANE = {
    "MARKDOWN_EXTRAS": [
        "fenced-code-blocks",
        "header-ids",
        "metadata",
        "strike",
        "tables",
        "task_list",
        "nofollow",
        "code-friendly",
        "footnotes",
        "numbering",
        "strike",
        "toc",
    ]
}
```

````{note}
When `coltrane` is integrated into an existing Django site the `coltrane` settings are used like a normal Django site. However, when `coltrane` is used as a static or standalone site (i.e. if there is an `app.py` file in the project folder), settings can be passed into the `initialize()` method in `app.py` as `kwargs`.

```python
# existing app.py file
wsgi = initialize(MARKDOWN_EXTRAS=["metadata",])
# rest of the app.py file
```

````

## Keys

### MARKDOWN_EXTRAS

The features that should be enabled when rendering markdown. A list of all available features: https://github.com/trentm/python-markdown2/wiki/Extras. The default extras are:

```python
[
    "fenced-code-blocks",
    "header-ids",
    "metadata",
    "strike",
    "tables",
    "task_list",
    "nofollow",
    "code-friendly",
    "footnotes",
    "numbering",
    "strike",
    "toc",
]
```

### VIEW_CACHE

Caches the rendered HTML when dynamically rendering. Enabled by adding the `SECONDS` key to a `VIEW_CACHE` dictionary. Not used for static sites.

#### SECONDS

Specifies how long the markdown should be cached when Django is dynamically serving the markdown.

```python
COLTRANE = {
    # other settings
    "VIEW_CACHE": {"SECONDS": 60 * 15},
}
```

#### CACHE_NAME

Specifies a name for the cache to use. Defaults to "default".

```python
COLTRANE = {
    # other settings
    "VIEW_CACHE": {"SECONDS": 60 * 15, "CACHE_NAME": "coltrane-view-cache"},
}
```
