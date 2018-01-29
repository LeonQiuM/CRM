#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Leon"
# Date: 2018/1/23
from django.db.models import Q


def table_filter(request, admin_class):
    """
    根据条件过滤并返回
    :param request:
    :param admin_class:
    :return:
    """
    filter_conditions = {}
    key_words = ['page', 'order', '_q']  # 分页关键字,排序关键字,搜索关键字
    for k, v in request.GET.items():
        if k in key_words:
            continue
        if v:
            filter_conditions[k] = v
    if admin_class.ordering:
        default_order_field = admin_class.ordering
    else:
        default_order_field = '-id'
    return admin_class.model.objects.filter(**filter_conditions).order_by(default_order_field), filter_conditions


def table_sort(request, objs):
    order_key = request.GET.get("order")
    if order_key:
        res = objs.order_by(order_key)
        if order_key.startswith('-'):
            order_key = order_key.strip('-')
        else:
            order_key = "-%s" % order_key
    else:
        res = objs
    return res, order_key


def table_search(request, admin_class, object_list):
    search_key = request.GET.get("_q")
    if search_key:
        q_obj = Q()
        q_obj.connector = "OR"
        for column in admin_class.search_fields:
            q_obj.children.append(("%s__contains" % column, search_key))

        res = object_list.filter(q_obj)
        return res, search_key
    else:
        return object_list, ""
