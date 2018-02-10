from django.conf.urls import url, include
from king_admin import views

urlpatterns = [
    url(r'^$', views.index, name='table_index'),
    url(r'^(?P<app>\w+)/(?P<table>\w+)/$', views.display_table_objs, name='table_objs'),
    url(r'^(?P<app>\w+)/(?P<table>\w+)/add/$', views.table_obj_add, name='table_obj_add'),
    url(r'^(?P<app>\w+)/(?P<table>\w+)/(?P<id>\d+)/change/$', views.table_obj_change, name='table_obj_change'),
    url(r'^(?P<app>\w+)/(?P<table>\w+)/(?P<id>\d+)/delete/$', views.table_obj_delete, name='obj_delete'),
]
