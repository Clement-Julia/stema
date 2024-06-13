from django import template

register = template.Library()

@register.filter
def format_number(value):
    try:
        value = int(value)
        return f"{value:,}".replace(",", " ")
    except (ValueError, TypeError):
        return value
