# Settings

Settings specified in a `COLTRANE` dictionary.

```python
# default `coltrane` settings
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
    EXTRA_FILE_NAMES=[],
}
```

````{note}
When `coltrane` is integrated into an existing Django site the `coltrane` settings are used like a normal Django site. However, when `coltrane` is used as a static or standalone site (i.e. if there is an `app.py` file in the project folder), settings can be passed into the `initialize()` method in `app.py` as `kwargs`.

```python
# existing app.py file
wsgi = initialize(MARKDOWN_EXTRAS=["metadata",], MISTUNE_PLUGINS=["table",])
# rest of the app.py file
```

````

## Keys

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

### SITE_URL

Because RSS requires an absolute URL, `coltrane` needs to know about the current domain for the site.

```python
COLTRANE = {
    # other settings
    "SITE_URL": "https://example.com",
}
```

### EXTRA_FILE_NAMES

Any additional non-markdown file names that should be included. The file names will be retrieved from the `content` directory and will be built or served (depending on the mode). This could be used for `robots.txt` or any other file that might need to be included. Defaults to an empty array.

```python
COLTRANE = {
    # other settings
    "EXTRA_FILE_NAMES": [],
}
```
