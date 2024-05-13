# Settings

Settings for `coltrane` are specified in a `COLTRANE` dictionary in the `settings.py` file. All [env settings](env.md) are available in the `COLTRANE` dictionary sans the leading "COLTRANE_", e.g. `COLTRANE_TITLE` in the `.env` file would be `COLTRANE.TITLE` in `settings.COLTRANE`.

```python
# settings.py

...

# Sample `coltrane` settings
COLTRANE = {
    "MISTUNE_PLUGINS": [
        "strikethrough",
        "footnotes",
        "table",
        "task_lists",
        "def_list",
        "abbr",
        "mark",
        "insert",
        "superscript",
        "subscript",
    ],
}

...
```

````{note}
`coltrane` settings can be passed into the `initialize()` method in `app.py` as `kwargs`.

```python
# existing app.py file
wsgi = initialize(MARKDOWN_EXTRAS=["metadata",], MISTUNE_PLUGINS=["table",])
# rest of the app.py file
```

````

## Keys

The keys below are specific to the `COLTRANE` dictionary `settings.py`. But, all [env settings](env.md) can be used.

### MISTUNE_PLUGINS

The features that should be enabled when rendering markdown with `mistune`. A list of all available features: https://mistune.lepture.com/en/latest/plugins.html. The default extras are:

```python
[
    "strikethrough",
    "footnotes",
    "table",
    "task_lists",
    "def_list",
    "abbr",
    "mark",
    "insert",
    "superscript",
    "subscript",
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
