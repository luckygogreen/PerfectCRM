from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from crm import models
# Create your views here.

@login_required
def dashboard(request):
    return render(request,'crm/dashboard.html')

@login_required
def customers(request):
    return render(request,'crm/customers.html')

@login_required
def stu_enrollment(request):
    print('程序运行到了stu_enrollment')
    geturl = request.get_port()
    print(geturl)
    return render(request, 'crm/stu_enrollment.html')
