#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Leon"
# Date: 2018/1/9

from django import template
from django.utils.safestring import mark_safe
import datetime

register = template.Library()


@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name


@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()


@register.simple_tag
def build_table_row(obj, admin_class):
    row_ele = ""
    for column in admin_class.list_display:
        filed_obj = obj._meta.get_field(column)
        if filed_obj.choices:
            column_data = getattr(obj, 'get_%s_display' % column)()
        else:
            column_data = getattr(obj, column)

        if type(column_data).__name__ == "datetime":
            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")
        row_ele += "<td>%s</td>" % (column_data)
    return mark_safe(row_ele)


@register.simple_tag
def render_page_ele(loop_counter, query_sets):
    if abs(query_sets.number - loop_counter) <= 2:
        if query_sets.number == loop_counter:
            ele = """<li class="active"><a href="?page=%s">%s</a></li>""" % (loop_counter, loop_counter)
        else:
            ele = """<li><a href="?page=%s">%s</a></li>""" % (loop_counter, loop_counter)
        return mark_safe(ele)
    else:
        return ''


@register.simple_tag
def render_filter_ele(condtion, admin_class, filter_conditions):
    select_ele = """<select class="form-control" name='%s'><option value=''>----</option>""" % condtion
    field_obj = admin_class.model._meta.get_field(condtion)
    if field_obj.choices:
        selectd = ""
        for choice_item in field_obj.choices:
            if filter_conditions.get(condtion) == str(choice_item[0]):
                selectd = "selected"
            select_ele += """<option value='%s' %s>%s</option>""" % (choice_item[0], selectd, choice_item[1])
            selectd = ""
    if type(field_obj).__name__ == "ForeignKey":
        selectd = ""
        for choice_item in field_obj.get_choices()[1:]:
            if filter_conditions.get(condtion) == str(choice_item[0]):
                selectd = "selected"
            select_ele += """<option value='%s' %s>%s</option>""" % (choice_item[0], selectd, choice_item[1])
            selectd = ""
    select_ele += "</select>"
    return mark_safe(select_ele)
