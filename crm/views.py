from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from crm import models
# Create your views here.

@login_required()
def dashboard(request):
    return render(request,'crm/dashboard.html')

def customers(request):
    return render(request,'crm/customers.html')
