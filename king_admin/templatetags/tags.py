#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Leon"
# Date: 2018/1/9

from django import template

register = template.Library()


@register.simple_tag()
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name
