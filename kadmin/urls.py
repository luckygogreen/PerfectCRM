
from django.conf.urls import url,include
from kadmin import views

urlpatterns = [
    url(r'^klogin/$', views.kuser_login),
    url(r'^klogout/$', views.kuser_logout),
    url(r'^$', views.kevin_index),
    url(r'^(\w+)/$', views.kapp,name='app_table'),
    url(r'^(\w+)/(\w+)/$', views.table_obj_list,name='table_obj_list'),
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_obj_change,name='table_obj_change'), #只有经过正则匹配才算参数
    url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.table_obj_delete,name='table_obj_delete'), #只有经过正则匹配才算参数
    url(r'^(\w+)/(\w+)/add/$', views.table_obj_add,name='table_obj_add'), #只有经过正则匹配才算参数

]
