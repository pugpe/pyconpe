# -*- coding:utf-8 -*-
# baseado em: http://djangosnippets.org/snippets/1586/
from django import template

register = template.Library()


@register.filter
def cssclass(form, name_arg):
    """
    Replace the attribute css class for Field 'name' with 'arg'.
    """
    name, arg = name_arg.split(':')
    form.fields[name].widget.attrs['class'] = arg

    return form


@register.filter
def fieldclass(field, arg):
    """
    Replace class of field
    """
    field.field.widget.attrs['class'] = arg
    return field
