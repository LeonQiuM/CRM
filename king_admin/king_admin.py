#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Leon"
# Date: 2018/1/9

from crm import models
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

enabled_admins = {}


class BaseAdmin(object):
    list_display = []  # 展示字段
    list_filters = []  # 多条件查询字段
    list_per_page = 5  # 单页数量
    search_fields = []  # 可搜索字段
    ordering = None  # 按照哪个排序
    filter_horizontal = []  # 外键复选框
    actions = ['delete_selected_objs']

    def delete_selected_objs(self, request, query_sets):
        objs = query_sets
        app = self.model._meta.app_label
        table = self.model._meta.model_name
        admin_class = self
        selected_ids = ','.join([str(i.id) for i in query_sets])
        if request.POST.get('delete_confirm') == "yes":
            query_sets.delete()
            return redirect(reverse("table_objs", kwargs={"app": app, "table": table}))
        action = request._admin_action
        return render(request, 'king_admin/table_obj_delete.html', locals())


class UserProfileAdmin(BaseAdmin):
    list_display = ['user', "name"]


class CustomerAdmin(BaseAdmin):
    list_display = ['id', 'qq', 'name', 'source', 'consultant', 'consult_course', 'status', 'date']
    list_filters = ['source', 'consultant', 'consult_course', 'status', 'date']
    search_fields = ['name', 'qq', 'consultant__name']
    list_per_page = 5
    ordering = 'date'
    filter_horizontal = ['tag']
    actions = ['delete_selected_objs', 'test']

    def test(self, request, query_sets):
        """测试动作"""
        print("in test")


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
