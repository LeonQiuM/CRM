#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Leon"
# Date: 2018/1/23


def table_filter(request, admin_class):
    """
    根据条件过滤并返回
    :param request:
    :param admin_class:
    :return:
    """
    filter_conditions = {}
    for k, v in request.GET.items():
        if v:
            filter_conditions[k] = v
        if k == "page" or k == 'order':  # 分页关键字,排序关键字
            del filter_conditions[k]
    print(filter_conditions)
    return admin_class.model.objects.filter(**filter_conditions), filter_conditions


def table_sort(request, objs):
    order_key = request.GET.get("order")
    if order_key and order_key.startswith('-'):
        return objs.order_by("-%s" % order_key)
    elif order_key:
        return objs.order_by(order_key)
