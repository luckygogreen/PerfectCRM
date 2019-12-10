from kadmin.kadmin_base import BaseKadmin

class KadminSite(object):
    def __init__(self):
        self.enabled_admins = {}


    def kregister(self,model_class,admin_class = None):
        """注册Admin表"""
        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name
        if not admin_class: #避免多个model共享同一个 BaseKadmin 内存对象
            admin_class = BaseKadmin()
        else:
            admin_class = admin_class()
        admin_class.model = model_class # 把model_class 赋值给admin_class.model ,此时的admin_class，就多一个一个model类，类里存的是model_class
        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name] = {}
        self.enabled_admins[app_name][model_name] = admin_class


ksite = KadminSite()