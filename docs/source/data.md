# Data

`coltrane` is designed to be used without a database, however, sometimes it's useful to have access to data inside your templates.

## JSON data directory

Create a directory named `data` in your project folder (if it doesn't already exist) and add JSON files. The name of the file (without the `json` extension) will be used as the key in the context data.

If there are JSON files in sub-directories, the directory names will be included in the dictionary hierarchy.

**`data/author.json`**

```JSON
{
    {"name": "Douglas Adams"}
}
```

**`data/books/book.json`**

```JSON
{
    {"title": "The Hitchhiker's Guide to the Galaxy"}
}
```

**`content/index.md`**

```markdown
# index

{{ data.author.name }} is the author.

{{ data.books.book.title }} is the book title.
```

**Generated `index.html`**

```html
<h1 id="index">index</h1>

<p>Douglas Adams is the author.</p>

<p>The Hitchhiker's Guide to the Galaxy is the book title.</p>
```

## JSON5 support

[JSON5](https://json5.org) data files are supported if the [`json5` extra](installation.md#json5) is installed and the [`COLTRANE_JSON5_DATA` environment setting](env.md#coltrane_data_json5) is set to `True`.
