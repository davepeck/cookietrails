from django import template

register = template.Library()


@register.filter
def get_item(dictionary: dict, key: str):
    return dictionary.get(key, 0)
