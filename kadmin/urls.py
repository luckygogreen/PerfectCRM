
from django.conf.urls import url,include
from kadmin import views

urlpatterns = [
    url(r'^$', views.kevin_index),
    url(r'^klogin/$', views.kuser_login),
    url(r'^klogout/$', views.kuser_logout),
    url(r'^(\w+)/(\w+)/$', views.table_obj_list,name='table_obj_list'),

]
