from kadmin.ksites import ksite
from student import models
from kadmin.kadmin_base import BaseKadmin

print('student下的Kingadmin已经被执行')

class AdminTest(BaseKadmin):
    list_display = ['id', 'name']


ksite.kregister(models.Test,AdminTest)