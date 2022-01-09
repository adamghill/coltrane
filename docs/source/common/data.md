# Data

`coltrane` is designed to be used without a database, however, sometimes it's useful to have access to data inside your templates. There are two ways to include dat ain your templates and they can be used separately or together.

```{note}
JSON data directory keys take precendence over the keys in `data.json`.
```

## JSON data file

Create a file named `data.json` in your project folder. Add whatever data you want to that file and it will be included in the template context in a `data` template variable.

**`data.json`**

```JSON
{
    {"answer": 42}
}
```

**`content/index.md`**

```markdown
# index

The answer to everything is {{ data.answer }}
```

**Generated `index.html`**

```html
<h1>index</h1>

<p>The answer to everything is 42</p>
```

## JSON data directory

Create a directory named `data` in your project folder and create JSON files in that directory. The name of the file (without the `json` extension) will be used as the key in the context data.

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
