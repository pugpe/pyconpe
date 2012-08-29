# -*- coding:utf-8 -*-
from django import template

register = template.Library()


@register.filter
def verbose_name(field, form):
    '''Get verbose_name of field from form'''
    return unicode(form._meta.model._meta.get_field(field).verbose_name)
