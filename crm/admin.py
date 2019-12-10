from django.contrib import admin

# Register your models here.
from  crm import models

class admin_CustomerInfo(admin.ModelAdmin):
    list_display = ['id','name','phone','address','wechat_or_other','source','cunsultant','status','date']
    list_filter = ['name','phone','source','cunsultant','wechat_or_other','consult_course']
    search_fields = ['id','name','phone','cunsultant__name']
    list_editable = ['source','status']


admin.site.register(models.CustomerInfo,admin_CustomerInfo)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.UserProfile)
admin.site.register(models.Role)
admin.site.register(models.Student)
admin.site.register(models.Course)
admin.site.register(models.ClassList)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)
admin.site.register(models.Branch)
admin.site.register(models.Menus)