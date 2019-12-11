from kadmin.ksites import ksite
from crm import models
from kadmin.kadmin_base import BaseKadmin


print('测试 crm 下的Kingadmin')


class admin_CustomerInfo(BaseKadmin):
    list_display = ['id', 'name', 'phone', 'address', 'wechat_or_other', 'source', 'cunsultant', 'status', 'date']
    list_filter = ['source', 'cunsultant', 'consult_course']
    search_fields = ['id', 'name', 'phone', 'cunsultant__name']
    list_editable = ['source', 'status']

class Admin_Menus(BaseKadmin):
    list_display = ['id', 'name', 'url_type', 'url']

ksite.kregister(models.CustomerInfo,admin_CustomerInfo)
ksite.kregister(models.Menus,Admin_Menus)
ksite.kregister(models.Role)