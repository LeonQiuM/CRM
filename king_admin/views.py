from django.shortcuts import render
from king_admin import king_admin
import importlib


# Create your views here.


def index(request):
    '''

    :param request:
    :return:
    '''
    if request.method == "GET":
        table_list = king_admin.enabled_admins
        print(table_list)
        return render(request, 'king_admin/table_index.html', locals())

    elif request.method == "POST":
        pass

    else:
        pass


def display_table_objs(request, app, table):
    '''

    :param request:
    :return:
    '''
    print(app,table)
    admin_class = king_admin.enabled_admins[app][table]
    if request.method == "GET":
        return render(request, 'king_admin/table_objs.html', locals())

    elif request.method == "POST":
        pass

    else:
        pass
