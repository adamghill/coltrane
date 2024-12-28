---
h1: Testing 1,2,3
numbers:
  - 1
  - 2
  - 3
number: 123456
test_string: this is a test string
---

# {{ h1 }}

```html
<!-- templates/home.html -->
{% extends 'base.html' %}
```

```javascript
function App() {
  return (
    <div style={{padding: "16px"}}>
      ...
    </div>
  );
}
```


This is a test

_ok_

**great**

## sub-heading

data.index.answer: {{ data.index.answer }}

data.index.author: {{ data.index.author }}

data.nested.more.another: {{ data.nested.more.another }}

Now: {{ now|date:"c" }}

For loop:

{% for i in numbers %}

- i: {{ i }}

{% endfor %}

Humanize built-in: {{ number|intcomma }}

Custom tag (should be "this is a string"): {{ test_string|cut_test:'test ' }}

Request: {{ request }}

Debug: {{ debug }}

![music]({% static 'images/music-note.svg' %})
