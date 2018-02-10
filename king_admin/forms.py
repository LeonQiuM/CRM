#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Leon"
# Date: 2018/1/28

from django import forms
from crm import models
from django.forms import ValidationError
from django.utils.translation import gettext as _


class CustomerModelForm(forms.ModelForm):
    model = models.Customer
    fields = "__all__"


def create_model_form(request, admin_class):
    """动态生成ModelForm"""

    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = "form-control"
            if field_name in admin_class.readonly_fields:
                field_obj.widget.attrs['disabled'] = 'disabled'
        return forms.ModelForm.__new__(cls)

    def default_clean(self):
        """给所有的 form 添加一个自定义 clean 验证"""
        cleaned_data = self.cleaned_data
        error_list = []
        for field in admin_class.readonly_fields:
            field_row_val = getattr(self.instance, field)
            field_new_val = cleaned_data.get(field)
            if field_new_val != field_row_val:
                error_list.append(
                    ValidationError(
                        _('field %(value)s is Readonly'),
                        code="invalid",
                        params={"value": field}
                    )
                )

        self.ValidationError = ValidationError
        # 触发用户自定义的 clean 验证 传入的为 form_obj
        res = admin_class.default_form_validation(self)  # 用户自己返回的错误信息收集
        if res:
            error_list.append(res)
        if error_list:  # 返回所有的错误信息
            raise ValidationError(error_list)

    class Meta:
        model = admin_class.model
        fields = "__all__"

    attrs = {"Meta": Meta}
    _model_form_class = type("DynamicModelForm", (forms.ModelForm,), attrs)
    setattr(_model_form_class, "__new__", __new__)
    setattr(_model_form_class, "clean", default_clean)
    return _model_form_class
