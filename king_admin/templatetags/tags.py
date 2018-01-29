#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Leon"
# Date: 2018/1/9

from django import template
from django.utils.safestring import mark_safe
from django.utils import timezone
import pytz

register = template.Library()


@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name


@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()


@register.simple_tag
def build_table_row(obj, admin_class, request):
    row_ele = ""
    for index, column in enumerate(admin_class.list_display):
        filed_obj = obj._meta.get_field(column)
        if filed_obj.choices:
            column_data = getattr(obj, 'get_%s_display' % column)()
        else:
            column_data = getattr(obj, column)

        if type(column_data).__name__ == "datetime":
            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")
        if index == 0:
            column_data = "<a href='%s%s/change/' >%s</a>" % (request.path, obj.id, column_data)
        row_ele += "<td>%s</td>" % (column_data)
    return mark_safe(row_ele)


@register.simple_tag
def render_page_ele(loop_counter, query_sets, filter_conditions):
    filters = ""
    for k, v in filter_conditions.items():
        if v:
            filters += "&%s=%s" % (k, v)

    if loop_counter < 3 or loop_counter > query_sets.paginator.num_pages - 2:  # 前两页，,后两页都要显示
        if query_sets.number == loop_counter:
            ele = """<li class="active"><a href="?page=%s">%s</a></li>""" % (loop_counter, loop_counter)
        else:
            ele = """<li><a href="?page=%s%s">%s</a></li>""" % (loop_counter, filters, loop_counter)
        return mark_safe(ele)

    if abs(query_sets.number - loop_counter) <= 2:
        if query_sets.number == loop_counter:
            ele = """<li class="active"><a href="?page=%s">%s</a></li>""" % (loop_counter, loop_counter)
        else:
            ele = """<li><a href="?page=%s%s">%s</a></li>""" % (loop_counter, filters, loop_counter)
        return mark_safe(ele)
    else:
        return ''


@register.simple_tag
def render_filter_ele(filter_field, admin_class, filter_conditions):
    select_ele = """<select class="form-control" name='{filter_field}'><option value=''>-ALL-</option>"""
    field_obj = admin_class.model._meta.get_field(filter_field)
    if field_obj.choices:
        selectd = ""
        for choice_item in field_obj.choices:
            if filter_conditions.get(filter_field) == str(choice_item[0]):
                selectd = "selected"
            select_ele += """<option value='%s' %s>%s</option>""" % (choice_item[0], selectd, choice_item[1])
            selectd = ""
    if type(field_obj).__name__ == "ForeignKey":
        selectd = ""
        for choice_item in field_obj.get_choices()[1:]:
            if filter_conditions.get(filter_field) == str(choice_item[0]):
                selectd = "selected"
            select_ele += """<option value='%s' %s>%s</option>""" % (choice_item[0], selectd, choice_item[1])
            selectd = ""

    if type(field_obj).__name__ in ["DateTimeField", "DateField"]:
        current_today = timezone.now().date()
        date_choiecs_lsit = []
        date_choiecs_lsit.append(["今天", current_today])
        date_choiecs_lsit.append(["近1天", current_today - timezone.timedelta(days=1)])
        date_choiecs_lsit.append(["近3天", current_today - timezone.timedelta(days=3)])
        date_choiecs_lsit.append(["近7天", current_today - timezone.timedelta(days=7)])
        date_choiecs_lsit.append(["本月", current_today.replace(day=1)])
        date_choiecs_lsit.append(["近30天", current_today - timezone.timedelta(days=30)])
        date_choiecs_lsit.append(["近90天", current_today - timezone.timedelta(days=90)])
        date_choiecs_lsit.append(["近180天", current_today - timezone.timedelta(days=180)])
        date_choiecs_lsit.append(["本年", current_today.replace(month=1, day=1)])
        date_choiecs_lsit.append(["近一年", current_today - timezone.timedelta(days=365)])
        selectd = ""
        for item in date_choiecs_lsit:
            if filter_conditions.get("%s__gte" % filter_field) == str(item[1]):
                selectd = "selected"
            select_ele += """<option value='%s' %s>%s</option>""" % (item[1], selectd, item[0])
            selectd = ""
        filter_field_name = "%s__gte" % (filter_field)
    else:
        filter_field_name = filter_field
    select_ele += "</select>"
    select_ele = select_ele.format(filter_field=filter_field_name)
    return mark_safe(select_ele)


@register.simple_tag
def build_paginators(query_sets, filter_conditions, previous_order, search_key):
    filter_conditions['order'] = previous_order
    filter_conditions['_q'] = search_key

    filters = page_btns = ""
    for k, v in filter_conditions.items():
        if v:
            filters += "&%s=%s" % (k, v)
    if query_sets.has_previous():
        prev_page_btn = '''<li class=""><a href="?page=%s%s">上一页</a></li>''' % (
            query_sets.previous_page_number(), filters
        )
    else:
        prev_page_btn = '''<li class="disabled"><span><span aria-hidden="true">上一页</span></span></li>'''

    if query_sets.has_next():
        last_page_btn = '''<li class=""><a href="?page=%s%s">下一页</a></li>''' % (
            query_sets.next_page_number(),
            filters
        )
    else:
        last_page_btn = '''<li class="disabled"><span><span aria-hidden="true">下一页</span></span></li>'''
    page_btns += """<li><a href="?page=1%s">首页</a></li>""" % (filters)
    page_btns += prev_page_btn
    flag_display = False
    for page_num in query_sets.paginator.page_range:
        if page_num < 3 or page_num > query_sets.paginator.num_pages - 2:  # 前两页和后两页
            if query_sets.number == page_num:
                page_btns += """<li class="active"><a href="?page=%s%s">%s</a></li>""" % (page_num, filters, page_num)
            else:
                page_btns += """<li><a href="?page=%s%s">%s</a></li>""" % (page_num, filters, page_num)
        elif abs(query_sets.number - page_num) <= 1:
            if query_sets.number == page_num:
                flag_display = False
                page_btns += """<li class="active"><a href="?page=%s%s">%s</a></li>""" % (page_num, filters, page_num)
            else:
                page_btns += """<li><a href="?page=%s%s">%s</a></li>""" % (page_num, filters, page_num)
        else:
            if not flag_display:
                flag_display = True
                page_btns += "<li><a>...</a></li>"
    page_btns += last_page_btn
    page_btns += """<li><a href="?page=99999999%s">首页</a></li>""" % (filters)
    return mark_safe(page_btns)


@register.simple_tag
def build_table_thead(column, order_key, filter_conditions):
    filters = ""
    for k, v in filter_conditions.items():
        if v:
            filters += "&%s=%s" % (k, v)
    ele = """
            <th>
                {column}<a href='?order={order_key}{filters}'>{sort_icon}</a>
            </th>
        """
    if order_key:
        if order_key.startswith('-'):
            sort_icon = '<span class="glyphicon glyphicon-sort-by-attributes pull-right"></span>'
        else:
            sort_icon = '<span class="glyphicon glyphicon-sort-by-attributes-alt pull-right"></span>'
        if order_key.strip('-') == column:
            order_key = order_key
        else:
            order_key = column
            sort_icon = '<span class="glyphicon glyphicon-sort pull-right" aria-hidden="true"></span>'
    else:  # 没有排序
        order_key = column
        sort_icon = '<span class="glyphicon glyphicon-sort pull-right" aria-hidden="true"></span>'
    ele = ele.format(order_key=order_key, filters=filters, column=column, sort_icon=sort_icon)

    return mark_safe(ele)


@register.simple_tag
def get_model_name(admin_class):
    return mark_safe(admin_class.model._meta.verbose_name)
