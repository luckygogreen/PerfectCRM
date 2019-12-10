from kadmin.ksites import ksite
from student import models
print('测试 student 下的 Kingadmin')

class AdminTest(object):
    list_display = ['id', 'name']


ksite.kregister(models.Test,AdminTest)