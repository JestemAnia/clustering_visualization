from django import template

register = template.Library()


# Custom template filters
@register.filter
def to_id(value):
    return value[:-3]


@register.filter
def to_name(value):
    return value[:-3].title()



