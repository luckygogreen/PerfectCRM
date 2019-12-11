from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from kadmin import kadd_stepup
kadd_stepup.kadmin_auto_deicover()
from kadmin.ksites import ksite
# print('ksite:',ksite.enabled_admins) #{'crm': {'customerinfo': <class 'crm.kingadmin.admin_CustomerInfo'>, 'menus': <class 'crm.kingadmin.Admin_Menus'>, 'role': <class 'kadmin.kadmin_base.BaseKadmin'>}, 'student': {'test': <class 'student.kingadmin.AdminTest'>}}
for k,v in ksite.enabled_admins.items():
    for table_name,admin_class in v.items():
        pass
        # print(table_name,':',id(admin_class))  # 打印admin_class 的内存地址


@login_required
def kevin_index(request):
    # print(conf.settings.INSTALLED_APPS)
    return render(request, 'kindex.html', {'ksite': ksite})

#排序
# str.startswith('-') #判断 字符串是否以减号开头
# str.strip('-') # 去掉字符串中的减号
def get_orderby_result(request,queryset,admin_class):
    current_order_column={}
    order_index = request.GET.get('_o')
    print(order_index)
    if order_index:
        order_index = int(order_index)
        orderby_key = admin_class.list_display[abs(order_index)-1]
        current_order_column[orderby_key] = order_index #让前段程序知道当前排序的列
        if order_index >= 0:
            return queryset.order_by(orderby_key),current_order_column
        else:
            return queryset.order_by('-%s' % orderby_key), current_order_column
    else:
        return queryset,current_order_column

#筛选
def get_filter_result(request,queryset):
    filter_condition = {}
    for k,v in request.GET.items():
        if k in ('_kpage','_o'):continue
        if v:
            filter_condition[k]=v
    print('filter_condition:',filter_condition)
    return queryset.filter(**filter_condition),filter_condition

@login_required
def table_obj_list(request, appname, modelname,show_items_per_page=2):
    """取出指定Model table里的数据，返回给前端"""
    # print(ksite.enabled_admins[appname][modelname])  # <class 'crm.kingadmin.admin_CustomerInfo'>
    # print(ksite.enabled_admins[appname][modelname].list_display)  # ['id', 'name', 'phone', 'address', 'wechat_or_other', 'source', 'cunsultant', 'status', 'date']
    # print(ksite.enabled_admins[appname][modelname].model.objects.all())  # <QuerySet [<CustomerInfo: 大海>, <CustomerInfo: 大地>, <CustomerInfo: 大气>]>
    admin_class = ksite.enabled_admins[appname][modelname]
    queryset = admin_class.model.objects.all()
    queryset,filter_condition = get_filter_result(request,queryset) #筛选
    admin_class.filter_condition = filter_condition

    queryset,current_order_column = get_orderby_result(request,queryset,admin_class) #排序

    paginator = Paginator(queryset, show_items_per_page)  # 分页
    page = request.GET.get('_kpage')
    queryset = paginator.get_page(page)

    return render(request,
                  'table_object_list.html',
                  {'queryset':queryset,
                   'admin_class':admin_class,
                   'appname':appname,
                   'modelname':modelname,
                   'show_items_per_page':show_items_per_page,
                   'current_order_column':current_order_column})

def kuser_login(request):
    error_message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', '/kadmin/'))
        else:
            error_message = 'Wrong user or password!'
            return render(request, 'klogin.html', {'error_message': error_message})
    return render(request, 'klogin.html')


def kuser_logout(request):
    logout(request)
    return redirect('/kadmin/klogin/')
