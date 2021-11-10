from django import template

register = template.Library()


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name.title()


@register.filter
def get_from_key(obj, key):
    return getattr(obj,key)
