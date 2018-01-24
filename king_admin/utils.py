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
        if k == "page":
            del filter_conditions[k]

    return admin_class.model.objects.filter(**filter_conditions), filter_conditions
