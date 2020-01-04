"""PerfectCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from crm import views

urlpatterns = [
    url(r'^$', views.dashboard, name='sales_dashboard'),  # 销售首页
    url(r'^customers/$', views.customers),  # 客户列表页
    url(r'^stu_enrollment/$', views.stu_enrollment, name="stu_enrollment"),
    url(r'^enrollment/(\d+)/$', views.enrollment, name="enrollment"),  # (\d+) 普通的列表参数
    # url(r'^enrollment/<?P(参数名)(\d+)>/$', views.enrollment, name="enrollment"),  # <?P(参数名)(\d+)>带关键字的参数
    url(r'^enrollment/(\d+)/fileupload/$', views.enrollment_fileupload, name="enrollment_fileupload"),

]
