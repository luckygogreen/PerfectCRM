from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from crm import models
# Create your views here.

@login_required()
def dashboard(request):
    return render(request,'crm/dashboard.html')

def useless_justtest(request):
    """【001】all 和 select_related用法一样，取的结果也是一样的"""
    showmessage1 = request.user.userprofile.role.all()
    showmessage2=request.user.userprofile.role.select_related()
    print(showmessage1)
    print(showmessage2)
    """【001】all 和 select_related用法一样，取的结果也是一样的"""

def customers(request):
    return render(request,'crm/customers.html')
