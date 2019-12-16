from kadmin.ksites import ksite
from crm import models
from kadmin.kadmin_base import BaseKadmin


print('crm下的Kingadmin已经被执行')


class admin_CustomerInfo(BaseKadmin):
    list_display = ['id', 'name', 'phone', 'address', 'wechat_or_other', 'source', 'cunsultant', 'status', 'date']
    list_filter = ['source', 'cunsultant', 'consult_course','status','date']
    search_fields = ['id', 'name', 'phone', 'cunsultant__name']
    # list_editable = ['source', 'status']
    readonly_fields = ['status']  #这里不能是主外键表
    list_per_page = 10
    filter_horizontal = ['consult_course',]
    actions = ['change_status',]

    def change_status(self, request, querysets):
        # print("kadmin action:", self, request, querysets)
        print('self:', self)
        print('request:', request)
        print('querysets:', querysets)
        print('request.POST:', request.POST)
        querysets.update(status=2)

class Admin_Menus(BaseKadmin):
    list_display = ['id', 'name', 'url_type', 'url']
    list_filter = ['url_type']
    actions = ['change_status', ]

    def change_status(self, request, querysets):
        # print("kadmin action:", self, request, querysets)
        print('self:', self)
        print('request:', request)
        print('querysets:', querysets)
        print('request.POST:', request.POST)
        querysets.update(url_type=1)

ksite.kregister(models.CustomerInfo,admin_CustomerInfo)
ksite.kregister(models.Menus,Admin_Menus)
ksite.kregister(models.Role)