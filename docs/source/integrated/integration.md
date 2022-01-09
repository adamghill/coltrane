# Integration

## Linking

Django templates can link to `coltrane` markdown content with the `url` template tag and the slug of the markdown file.

```html
<!-- this href with link a route which renders the /content/about.md markdown file -->
<a href="{% url 'coltrane:content' 'about' %}">About</a>
```
