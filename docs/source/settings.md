# Settings

Settings for `coltrane` are specified in a `COLTRANE` dictionary in the `settings.py` file. All [env settings](env.md) are available to be set directly. Just remove the leading "COLTRANE_" from the environment name if applicable.

```python
# settings.py

...

# Sample `coltrane` settings
COLTRANE = {
    "MARKDOWN_RENDERER": "markdown2",
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
    ],
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

### MARKDOWN_RENDERER

Which markdown renderer to use. Value can be either "markdown2" or "mistune". The default for 0.22.0 and below is [`markdown2`](https://github.com/trentm/python-markdown2). After that it will be [`mistune`](https://github.com/lepture/mistune).

To enable `mistune` for version 0.22.0:
1. `poetry install --extras mistune`
2. Add `COLTRANE["MARKDOWN_RENDERER"] = "mistune"` to settings

### MARKDOWN_EXTRAS

The features that should be enabled when rendering markdown with `markdown2`. A list of all available features: https://github.com/trentm/python-markdown2/wiki/Extras. The default extras are:

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
