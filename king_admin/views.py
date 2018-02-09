from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from king_admin import king_admin, forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from king_admin.utils import table_filter, table_sort, table_search


# Create your views here.


def index(request):
    """

    :param request:
    :return:
    """
    if request.method == "GET":
        table_list = king_admin.enabled_admins
        return render(request, 'king_admin/table_index.html', locals())

    elif request.method == "POST":
        pass

    else:
        pass


def display_table_objs(request, app, table):
    """

    :param request:
    :return:
    """

    if request.method == "GET":
        admin_class = king_admin.enabled_admins[app][table]
        model = admin_class.model
        object_list, filter_conditions = table_filter(request, admin_class)  # 过滤

        object_list, search_key = table_search(request, admin_class, object_list)
        order_key = ""

        object_list, order_key = table_sort(request, object_list)  # 排序

        paginator = Paginator(object_list, admin_class.list_per_page)
        page = request.GET.get('page')
        try:
            query_sets = paginator.page(page)
        except PageNotAnInteger:
            # 不是int的值，显示第一页
            query_sets = paginator.page(1)
        except EmptyPage:
            # 超过限制，显示最后一页
            query_sets = paginator.page(paginator.num_pages)
        previous_order = request.GET.get('order', "")
        return render(request, 'king_admin/table_objs.html', locals())

    elif request.method == "POST":
        pass

    else:
        pass


def table_obj_change(request, app, table, id):
    """

    :param request:
    :return:
    """
    admin_class = king_admin.enabled_admins[app][table]
    model_form_class = forms.create_model_form(request, admin_class)
    query_set = admin_class.model.objects.get(id=id)

    if request.method == "GET":
        form_obj = model_form_class(instance=query_set)

        return render(request, 'king_admin/table_obj_change.html', locals())

    elif request.method == "POST":
        form_obj = model_form_class(request.POST, instance=query_set)
        if form_obj.is_valid():
            form_obj.save()
        return render(request, 'king_admin/table_obj_change.html', locals())
    else:
        pass


def table_obj_delete(request, app, table, id):
    """

    :param request:
    :return:
    """

    admin_class = king_admin.enabled_admins[app][table]
    obj = admin_class.model.objects.get(id=id)
    if request.method == "POST":
        obj.delete()
        return redirect(reverse('table_objs', kwargs={"app": app, "table": table}))
    return render(request, "king_admin/table_obj_delete.html", locals())


def table_obj_add(request, app, table):
    """

    :param request:
    :return:
    """
    admin_class = king_admin.enabled_admins[app][table]
    model_form_class = forms.create_model_form(request, admin_class)
    if request.method == "POST":
        form_obj = model_form_class(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('table_objs', kwargs={"app": app, "table": table}))
    else:

        form_obj = model_form_class()
    return render(request, 'king_admin/table_obj_add.html', {"form_obj": form_obj, "admin_class": admin_class})
