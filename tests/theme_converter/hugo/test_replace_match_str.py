import re

from coltrane.theme_converters.hugo import replace_match_str


def test_replace_match_str():
    expected = "111 {{ test replacement }} 222 {{ second test }} 333"

    original_string = "111 {{ first test }} 222 {{ second test }} 333"
    replacement_string = "{{ test replacement }}"

    matches = re.finditer(r"\{\{\s(first)\s(test)\s\}\}", original_string)
    match = next(matches)
    assert match, "Match is expected"

    actual = replace_match_str(original_string, match, 0, replacement_string)

    assert actual == expected
