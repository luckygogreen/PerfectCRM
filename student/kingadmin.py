from kadmin.ksites import ksite
from student import models
print('student下的Kingadmin已经被执行')

class AdminTest(object):
    list_display = ['id', 'name']


ksite.kregister(models.Test,AdminTest)