import pytest

from coltrane.theme_converters.hugo import convert_template_html


@pytest.mark.skip()
def test_loop_html():
    expected = '{% for _ in Pages.GroupByDate|"January" %}test{% endfor %}'

    template_html = """
{{- range .Pages.GroupByDate "January" }}
  <div class="archive-month">
    <h3 class="archive-month-header" id="{{ $year }}-{{ .Key }}">
      <a class="archive-header-link" href="#{{ $year }}-{{ .Key }}">
        {{- .Key -}}
      </a>
      <sup class="archive-count">&nbsp;{{ len .Pages }}</sup>
    </h3>
    <div class="archive-posts">
      {{- range .Pages }}
      {{- if eq .Kind "page" }}
      <div class="archive-entry">
        <h3 class="archive-entry-title entry-hint-parent">
          {{- .Title | markdownify }}
          {{- if .Draft }}
          <span class="entry-hint" title="Draft">
            <svg xmlns="http://www.w3.org/2000/svg" height="15" viewBox="0 -960 960 960" fill="currentColor">
              <path
                d="M160-410v-60h300v60H160Zm0-165v-60h470v60H160Zm0-165v-60h470v60H160Zm360 580v-123l221-220q9-9 20-13t22-4q12 0 23 4.5t20 13.5l37 37q9 9 13 20t4 22q0 11-4.5 22.5T862.09-380L643-160H520Zm300-263-37-37 37 37ZM580-220h38l121-122-18-19-19-18-122 121v38Zm141-141-19-18 37 37-18-19Z" />
            </svg>
          </span>
          {{- end }}
        </h3>
        <div class="archive-meta">
          {{- partial "post_meta.html" . -}}
        </div>
        <a class="entry-link" aria-label="post link to {{ .Title | plainify }}" href="{{ .Permalink }}"></a>
      </div>
      {{- end }}
      {{- end }}
    </div>
  </div>
  {{- end }}
"""
    actual = convert_template_html(template_html)

    assert actual == expected


@pytest.mark.skip()
def test_base_example():
    expected = """<!DOCTYPE html>
<html lang="{% get_current_language %}" dir="auto">

<head>
    {% include "partials/head.html" %}
</head>

<body class="
{% if not request.resolver_match.url_name == 'page' or request.resolver_match.url_name in ['archives', 'search'] %}
list
{% endif %}
{% if default_theme == 'dark' %}
dark
{% endif %}
" id="top">
    {% include "partials/header.html" %}
    <main class="main">
        {% block main %}
        {% endblock %}
    </main>
    {% include "partials/footer.html" %}
</body>

</html>
"""

    template_html = """{{- if lt hugo.Version "0.112.4" }}
{{- errorf "=> hugo v0.112.4 or greater is required for hugo-PaperMod to build " }}
{{- end -}}

<!DOCTYPE html>
<html lang="{{ site.Language }}" dir="{{ .Language.LanguageDirection | default "auto" }}">

<head>
    {{- partial "head.html" . }}
</head>

<body class="
{{- if (or (ne .Kind `page` ) (eq .Layout `archives`) (eq .Layout `search`)) -}}
{{- print "list" -}}
{{- end -}}
{{- if eq site.Params.defaultTheme `dark` -}}
{{- print " dark" }}
{{- end -}}
" id="top">
    {{- partialCached "header.html" . .Page -}}
    <main class="main">
        {{- block "main" . }}{{ end }}
    </main>
    {{ partialCached "footer.html" . .Layout .Kind (.Param "hideFooter") (.Param "ShowCodeCopyButtons") -}}
</body>

</html>
"""

    actual = convert_template_html(template_html)

    assert actual == expected
