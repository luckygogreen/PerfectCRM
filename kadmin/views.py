from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from kadmin import kadd_stepup
kadd_stepup.kadmin_auto_deicover()
from kadmin.ksites import ksite
print('ksite:',ksite.enabled_admins) #{'crm': {'customerinfo': <class 'crm.kingadmin.admin_CustomerInfo'>, 'menus': <class 'crm.kingadmin.Admin_Menus'>, 'role': <class 'kadmin.kadmin_base.BaseKadmin'>}, 'student': {'test': <class 'student.kingadmin.AdminTest'>}}
for k,v in ksite.enabled_admins.items():
    for table_name,admin_class in v.items():
        print(table_name,':',id(admin_class))  # 打印admin_class 的内存地址


@login_required
def kevin_index(request):
    # print(conf.settings.INSTALLED_APPS)
    return render(request, 'kindex.html', {'ksite': ksite})


@login_required
def table_obj_list(request, appname, modelname):
    """取出指定Model table里的数据，返回给前端"""
    print(ksite.enabled_admins[appname][modelname])  # <class 'crm.kingadmin.admin_CustomerInfo'>
    # print(ksite.enabled_admins[appname][modelname].list_display)  # ['id', 'name', 'phone', 'address', 'wechat_or_other', 'source', 'cunsultant', 'status', 'date']
    print(ksite.enabled_admins[appname][
              modelname].model.objects.all())  # <QuerySet [<CustomerInfo: 大海>, <CustomerInfo: 大地>, <CustomerInfo: 大气>]>
    admin_class = ksite.enabled_admins[appname][modelname]
    queryset = admin_class.model.objects.all()
    return render(request,'table_object_list.html',{'queryset':queryset,'admin_class':admin_class})

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
