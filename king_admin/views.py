from django.shortcuts import render
from king_admin import king_admin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from king_admin.utils import table_filter, table_sort


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
        # object_list = admin_class.model.objects.all()
        object_list, filter_conditions = table_filter(request, admin_class)  # 过滤
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

        return render(request, 'king_admin/table_objs.html', locals())

    elif request.method == "POST":
        pass

    else:
        pass
