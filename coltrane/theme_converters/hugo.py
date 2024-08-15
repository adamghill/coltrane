import re


def convert_files():
    """
    rename baseof.html to base.html
    """

    pass


def convert_template_html(template_html: str):
    # # Define regex patterns for Go template constructs
    # patterns = {
    #     # Includes (partials)
    #     r'{{\s*partial\s*"([a-zA-Z0-9_/.]+)"\s*\.\s*}}': r'{% include "\1" %}',
    #     # Loops
    #     r"{{\s*range\s*\.\s*([a-zA-Z0-9_]+)\s*}}": r"{% for \1 in \1 %}",
    #     # If statements
    #     r"{{\s*if\s*\.\s*([a-zA-Z0-9_]+)\s*}}": r"{% if \1 %}",
    #     r"{{\s*else\s*}}": r"{% else %}",
    #     # r"{{\s*end\s*}}": r"{% endif %}",
    # }

    # # Apply replacements
    # for pattern, replacement in patterns.items():
    #     template_str = re.sub(pattern, replacement, template_str)

    # return template_str

    # Convert variables
    variable_re = r"\{\{\s*\.([a-zA-Z0-9_]+)\s*\}\}"
    variable_sub = r"{{ \1 }}"
    template_html = re.sub(variable_re, variable_sub, template_html)

    # Convert blocks
    block_re = r'\{\{-?\s*block\s*"([a-zA-Z0-9_]+)"\s*\.\s*\}\}(.*?)\{\{\s*end\s*\}\}'
    block_sub = r"{% block \1 %}\2{% endblock %}"
    template_html = re.sub(block_re, block_sub, template_html)

    # Convert loops
    loop_re = r"\{\{-?\s*range\s+\.(([a-zA-Z0-9_\.\"\s])+?)\s*\}\}(.*?)\{\{\s*end\s*\}\}"
    loop_sub = r"{% for _ in \1 %}"
    template_html = re.sub(loop_re, loop_sub, template_html)

    # Convert if statements
    if_re = r"{{\*\s*(.*?)\s*\*}}"
    if_sub = r"{# \1 #}"
    template_html = re.sub(if_re, if_sub, template_html)

    # Convert 1-line comments
    comment_re = r"\{\{\*\s*(.*?)\s*\*\}\}"
    comment_sub = r"{# \1 #}"
    template_html = re.sub(comment_re, comment_sub, template_html)

    return template_html
