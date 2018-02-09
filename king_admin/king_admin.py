#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Leon"
# Date: 2018/1/9

from crm import models

enabled_admins = {}


class BaseAdmin(object):
    list_display = []  # 展示字段
    list_filters = []  # 多条件查询字段
    list_per_page = 5  # 单页数量
    search_fields = []  # 可搜索字段
    ordering = None  # 按照哪个排序
    filter_horizontal = []  # 外键复选框


class UserProfileAdmin(BaseAdmin):
    list_display = ['user', "name"]


class CustomerAdmin(BaseAdmin):
    list_display = ['id', 'qq', 'name', 'source', 'consultant', 'consult_course', 'status', 'date']
    list_filters = ['source', 'consultant', 'consult_course', 'status', 'date']
    search_fields = ['name', 'qq', 'consultant__name']
    list_per_page = 5
    ordering = 'date'
    filter_horizontal = ['tag']


class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ['customer', 'consultant', 'date']


def register(model_class, admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}

    admin_class.model = model_class  # 绑定model对象和自定义admin类
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class


register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)
register(models.UserProfile, UserProfileAdmin)
