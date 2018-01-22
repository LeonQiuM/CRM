#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Leon"
# Date: 2018/1/9

from crm import models

enabled_admins = {}


class BaseAdmin(object):
    list_display = []
    list_filter = []


class CustomerAdmin(BaseAdmin):
    list_display = ['qq', 'name', 'source', 'consultant', 'consult_course', 'status', 'date']


class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ['customer', 'consultant', 'date']


'''
@staticmethod
class admin_c(object):
    def __init__(self, model_class, your_class):
        self.model = your_class
        self.model_class = model_class
        self.enabled_admins = {}

    def register(self):
        if self.model_class._meta.app_label not in self.enabled_admins: # app
            self.enabled_admins[self.model_class._meta.app_label] = {}
        
        return self.enabled_admins
'''


def register(model_class, admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}

    admin_class.model = model_class  # 绑定model对象和自定义admin类
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class


register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)
