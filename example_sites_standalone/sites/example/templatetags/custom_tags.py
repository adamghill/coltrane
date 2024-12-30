from django import template

register = template.Library()


@register.filter(name="cut_test")
def cut_test(value, arg):
    return value.replace(arg, "")
