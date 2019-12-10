from django import conf
from kadmin.ksites import ksite
from crm import models

def kadmin_auto_deicover():
    for appname in conf.settings.INSTALLED_APPS:
        try:
            mob = __import__('{}.kingadmin'.format(appname))
            # print('mob:',mob)
        except ImportError:
            pass