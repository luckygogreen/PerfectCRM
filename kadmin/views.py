from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from crm import models
from django import conf
import importlib

# Create your views here.
def kuser_login(request):
    error_message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect(request.GET.get('next','/kadmin/'))
        else:
            error_message = 'Wrong user or password!'
            return render(request, 'klogin.html',{'error_message':error_message})
    return render(request, 'klogin.html')

def kuser_logout(request):
    logout(request)
    return redirect('/kadmin/klogin/')

@login_required()
def kevin_index(request):
    for appname in conf.settings.INSTALLED_APPS:
        try:
            print('appname:',appname)
            mob = __import__('{}.kingadmin'.format(appname))
            print('mob:',mob)
            print('mob.kingadmin:',mob.kingadmin)
        except ImportError:
            pass
    return render(request, 'kindex.html')