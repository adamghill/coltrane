import re
from collections import deque
from dataclasses import dataclass
from typing import Optional

GO_TEMPLATE_RE = re.compile(r"\{\{-?\s*(([^\s(\}\}\*)]+\s*?)*?)\s*\}\}")


def convert_files():
    """
    rename baseof.html to base.html
    """

    pass


def replace_match_str(s: str, match: re.Match, change_difference: int, replacement: str) -> str:
    start_with_change_difference = match.start() + change_difference
    end_with_change_difference = match.end() + change_difference

    return s[:start_with_change_difference] + replacement + s[end_with_change_difference:]


def _calculate_change_difference(replacement: str, match: re.Match):
    return len(replacement) - (match.end() - match.start())


def _get_action_and_expression(match):
    action = match.group(1)
    action_pieces = action.split(" ")
    expression = None

    if action_pieces:
        action = action_pieces[0]

        for idx, piece in enumerate(action_pieces[1:]):
            if piece.startswith("."):
                action_pieces[idx + 1] = piece[1:]

    # TODO: Handle more than 3 pieces? i.e. more than one argument?
    if len(action_pieces) == 3:
        if action_pieces[2] == "" or action_pieces[2] == ".":
            expression = action_pieces[1]
        else:
            expression = f"{action_pieces[1]}|{action_pieces[2]}"
    elif len(action_pieces) == 2:
        expression = action_pieces[1]

    return action, expression


@dataclass
class Action:
    action_name: str

    def get_django_replacement(self, expression: Optional[str]) -> str:
        raise NotImplementedError()

    def set_action_queue(self, action_queue: deque):
        self.action_queue = action_queue

    def push_action_on_queue(self):
        assert self.action_queue is not None, "action_queue must be set first"
        self.action_queue.append(self.action_name)


@dataclass
class Range(Action):
    def __init__(self):
        super().__init__(action_name="range")

    def get_django_replacement(self, expression: Optional[str]) -> str:
        if expression is None:
            raise AssertionError("Range requires an expression")

        self.push_action_on_queue()

        return f"{{% for _ in {expression} %}}"


@dataclass
class Block(Action):
    def __init__(self):
        super().__init__(action_name="block")

    def get_django_replacement(self, expression: Optional[str]) -> str:
        if expression is None:
            raise AssertionError("Expression requires a name")

        if (expression.startswith('"') and expression.endswith('"')) or (
            expression.startswith("'") and expression.endswith("'")
        ):
            expression = expression[1:-1]

        self.push_action_on_queue()

        return f"{{% block {expression} %}}"


@dataclass
class If(Action):
    def __init__(self):
        super().__init__(action_name="if")

    def get_django_replacement(self, expression: Optional[str]) -> str:
        if expression is None:
            raise AssertionError("If conditional requires an expression")

        self.push_action_on_queue()

        return f"{{% if {expression} %}}"


@dataclass
class End(Action):
    def __init__(self):
        super().__init__(action_name="end")

    def get_django_replacement(self, expression: Optional[str]) -> str:
        if not self.action_queue:
            raise Exception("end not applicable here")

        django_replacement = None
        previous_action = self.action_queue.pop()

        if previous_action == "range":
            django_replacement = "{% endfor %}"
        elif previous_action == "block":
            django_replacement = "{% endblock %}"
        elif previous_action == "if":
            django_replacement = "{% endif %}"
        else:
            raise AssertionError(f"Unknown previous action: '{previous_action}'")

        return django_replacement


action_handlers: list[Action] = [Range(), Block(), If(), End()]


def handle_go_constructs(html: str) -> str:
    # Store a list of actions in a queue
    action_queue = deque()

    # The string that replaces pieces might be a different length, so keep track of the difference is length
    # This gets used when replacing the pieces whose indexes need to be adjusted based on previous changes
    index_adjustment = 0
    django_replacement = ""

    for match in GO_TEMPLATE_RE.finditer(html):
        (action, expression) = _get_action_and_expression(match)
        action_handler = next(filter(lambda a: a.action_name == action, action_handlers), None)

        if action_handler:
            action_handler.set_action_queue(action_queue)
            django_replacement = action_handler.get_django_replacement(expression)

            html = replace_match_str(html, match, index_adjustment, django_replacement)
        else:
            variable = action

            if variable.startswith("."):
                variable = variable[1:]

            django_replacement = "{{ " + variable + " }}"
            html = replace_match_str(html, match, index_adjustment, django_replacement)

        change_difference = _calculate_change_difference(django_replacement, match)
        index_adjustment += change_difference

    return html


"""
TODO:
- support `-` to remove all blank strings or whatever it does
"""


def convert_template_html(template_html: str):
    # # Define regex patterns for Go template constructs
    # patterns = {
    #     # Includes (partials)
    #     r'{{\s*partial\s*"([a-zA-Z0-9_/.]+)"\s*\.\s*}}': r'{% include "\1" %}',
    #     # If statements
    #     r"{{\s*if\s*\.\s*([a-zA-Z0-9_]+)\s*}}": r"{% if \1 %}",
    #     r"{{\s*else\s*}}": r"{% else %}",
    #     # r"{{\s*end\s*}}": r"{% endif %}",
    # }

    # Convert 1-line comments
    comment_re = r"\{\{\*\s*(.*?)\s*\*\}\}"
    comment_sub = r"{# \1 #}"
    template_html = re.sub(comment_re, comment_sub, template_html)

    template_html = handle_go_constructs(template_html)

    return template_html
