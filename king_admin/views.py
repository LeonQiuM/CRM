from django.shortcuts import render
from king_admin import king_admin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def index(request):
    """

    :param request:
    :return:
    """
    if request.method == "GET":
        table_list = king_admin.enabled_admins
        print(table_list)
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
    print(app, table)
    admin_class = king_admin.enabled_admins[app][table]
    model = admin_class.model
    if request.method == "GET":
        object_list = admin_class.model.objects.all()
        paginator = Paginator(object_list, 5)
        page = request.GET.get('page')
        try:
            query_sets = paginator.page(page)
        except PageNotAnInteger:
            # 不是int的值，显示第一页
            query_sets = paginator.page(1)
        except EmptyPage:
            # 超过限制，显示最后一页
            query_sets = paginator.page(paginator.num_pages)

        return render(request, 'king_admin/table_objs.html', {'admin_class': admin_class, 'query_sets': query_sets})

    elif request.method == "POST":
        pass

    else:
        pass
