print('测试 student 下的 Kingadmin')

class AdminTest(object):
    list_display = ['id','name','phone','address','wechat_or_other','source','cunsultant','status','date']
    list_filter = ['name','phone','source','cunsultant','wechat_or_other','consult_course']
    search_fields = ['id','name','phone','cunsultant__name']
    list_editable = ['source','status']


# admin.site.register(models.CustomerInfo,AdminTest)