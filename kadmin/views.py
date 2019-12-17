import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from kadmin import kadd_stepup
from django.db.models import Q
from kadmin import dynamic_form

kadd_stepup.kadmin_auto_deicover()
from kadmin.ksites import ksite

# print('ksite:',ksite.enabled_admins) #{'crm': {'customerinfo': <class 'crm.kingadmin.admin_CustomerInfo'>, 'menus': <class 'crm.kingadmin.Admin_Menus'>, 'role': <class 'kadmin.kadmin_base.BaseKadmin'>}, 'student': {'test': <class 'student.kingadmin.AdminTest'>}}
for k, v in ksite.enabled_admins.items():
    for table_name, admin_class in v.items():
        pass
        # print(table_name, ':', id(admin_class))  # 打印admin_class 的内存地址


@login_required
def kevin_index(request):
    # print(conf.settings.INSTALLED_APPS)
    return render(request, 'kindex.html', {'ksite': ksite})

def kapp(request,appname):
    showapp = ksite.enabled_admins.get(appname)
    return render(request,'kapp.html',{'showapp': showapp,'appname':appname})


# 搜索
def get_search_result(request, queryset, admin_class):
    search_key = request.GET.get('_q')
    if search_key:
        q = Q()
        q.connector = 'or'
        for search_filed in admin_class.search_fields:
            q.children.append(('%s__icontains' % search_filed, search_key))  # q.children.append 里面必须是元祖
        return queryset.filter(q), search_key
    else:
        search_key = ''
        return queryset, search_key


# 排序
# str.startswith('-') #判断 字符串是否以减号开头
# str.strip('-') # 去掉字符串中的减号
def get_orderby_result(request, queryset, admin_class):
    current_order_column = {}
    order_index = request.GET.get('_o')
    if order_index:
        order_index = int(order_index)
        orderby_key = admin_class.list_display[abs(order_index) - 1]
        current_order_column[orderby_key] = order_index  # 让前段程序知道当前排序的列
        if order_index >= 0:
            return queryset.order_by(orderby_key), current_order_column
        else:
            return queryset.order_by('-%s' % orderby_key), current_order_column
    else:
        return queryset, current_order_column


# 筛选
def get_filter_result(request, queryset):
    filter_condition = {}
    for k, v in request.GET.items():
        if k in ('_kpage', '_o', '_q'): continue
        if v:
            filter_condition[k] = v
    print('filter_condition:', filter_condition)
    return queryset.filter(**filter_condition), filter_condition


@login_required  # 显示数据
def table_obj_list(request, appname, modelname):
    """取出指定Model table里的数据，返回给前端"""
    # print(ksite.enabled_admins[appname][modelname])  # <class 'crm.kingadmin.admin_CustomerInfo'>
    # print(ksite.enabled_admins[appname][modelname].list_display)  # ['id', 'name', 'phone', 'address', 'wechat_or_other', 'source', 'cunsultant', 'status', 'date']
    # print(ksite.enabled_admins[appname][modelname].model.objects.all())  # <QuerySet [<CustomerInfo: 大海>, <CustomerInfo: 大地>, <CustomerInfo: 大气>]>

    admin_class = ksite.enabled_admins[appname][modelname]
    if request.method == "POST":
        print(request.POST)
        selected_action = request.POST.get('action')
        selected_ids = json.loads(request.POST.get('selected_ids'))
        print(selected_action, selected_ids)
        if not selected_action:  # 如果有action参数,代表这是一个正常的action,如果没有,代表可能是一个删除动作
            if selected_ids:  # 这些选中的数据都要被删除
                admin_class.model.objects.filter(id__in=selected_ids).delete()
        else:  # 走action流程
            selected_objs = admin_class.model.objects.filter(id__in=selected_ids)
            admin_action_func = getattr(admin_class, selected_action)
            response = admin_action_func(request, selected_objs)
            if response:
                return response
    queryset = admin_class.model.objects.all().order_by('-id')
    queryset, filter_condition = get_filter_result(request, queryset)  # 筛选
    admin_class.filter_condition = filter_condition
    queryset, search_key = get_search_result(request, queryset, admin_class)  # 搜索
    admin_class.search_key = search_key
    queryset, current_order_column = get_orderby_result(request, queryset, admin_class)  # 排序
    paginator = Paginator(queryset, admin_class.list_per_page)  # 分页
    page = request.GET.get('_kpage')
    queryset = paginator.get_page(page)
    return render(request,
                  'table_object_list.html',
                  {'queryset': queryset,
                   'admin_class': admin_class,
                   'appname': appname,
                   'modelname': modelname,
                   'show_items_per_page': admin_class.list_per_page,
                   'current_order_column': current_order_column})


@login_required  # 修改数据
def table_obj_change(request, appname, modelname, changeid):
    """修改显示列表，返回的要修改的数"""
    admin_class = ksite.enabled_admins[appname][modelname]
    model_form = dynamic_form.create_dynamic_model_form(admin_class)
    model_obj = admin_class.model.objects.get(id=changeid)
    if request.method == 'GET':
        form_obj = model_form(instance=model_obj)
    elif request.method == 'POST':
        form_obj = model_form(instance=model_obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/kadmin/%s/%s/' % (appname, modelname))

    return render(request, 'table_object_change.html', locals())

@login_required
def table_obj_add(request,appname,modelname):
    admin_class = ksite.enabled_admins[appname][modelname]
    model_form = dynamic_form.create_dynamic_model_form(admin_class, form_add=True)
    if request.method == 'GET':
        form_obj = model_form()
    elif request.method == 'POST':
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
        return redirect('/kadmin/%s/%s/' % (appname, modelname))
    return render(request,'table_obj_add.html',locals())

@login_required
def table_obj_delete(request,appname,modelname,delete_id):
    admin_class = ksite.enabled_admins[appname][modelname]
    delete_obj = admin_class.model.objects.get(id=delete_id)
    if request.method == 'POST':
        delete_obj.delete()
        return redirect('/kadmin/%s/%s/'% (appname,modelname))
    return render(request,'table_object_delete.html',locals())

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
    print('111')
    logout(request)
    return redirect('/kadmin/klogin/')
