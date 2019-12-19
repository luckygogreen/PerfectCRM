import json
import datetime
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django import conf
from crm import models
from crm.forms import CustomerForm
# from django.utils.timezone import datetime
import os


# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'crm/dashboard.html')


@login_required
def customers(request):
    return render(request, 'crm/customers.html')


@login_required
def stu_enrollment(request):
    print('程序运行到了stu_enrollment')
    get_hosturl = request.get_host()
    customers = models.CustomerInfo.objects.all()
    class_list = models.ClassList.objects.all()
    if request.method == 'POST':
        customer_id = request.POST.get('customers_id')
        class_id = request.POST.get('class_id')
        enrollment_obj = models.StudentEnrollment.objects.create(
            customer_id=customer_id,
            class_grade_id=class_id,
            consulant_id=request.user.userprofile.id
        )
        print(enrollment_obj.id)
        enrollment_link = get_hosturl + '/crm/enrollment/{}/'.format(enrollment_obj.id)
    # get_enrollment_link = get_hosturl/
    return render(request, 'crm/stu_enrollment.html', locals())


def enrollment(request, enrollment_id):
    """学院在线报名表"""
    print('程序以及进入enrollment页面')
    enrollment_obj = models.StudentEnrollment.objects.get(id=enrollment_id)
    if enrollment_obj.contract_agreed == True:
        return HttpResponse('您已经提交了注册，申请正在审核中，请耐心等待！')
    if request.method == 'POST':
        print(request.POST)
        customers_form = CustomerForm(instance=enrollment_obj.customer, data=request.POST)
        if customers_form.is_valid():
            customers_form.save()
            enrollment_obj.contract_agreed = True
            enrollment_obj.contract_sign_date = datetime.datetime.now()
            enrollment_obj.save()
            return HttpResponse('你已经注册成功，请等待咨询顾问与你联系')
        else:
            print('验证失败:', customers_form.errors)
    else:
        customers_form = CustomerForm(instance=enrollment_obj.customer)

    upload_files = []
    conf_dir = conf.settings.CRM_FILE_UPLOADS_DIR[0]
    enrollment_upload_dir = os.path.join(conf_dir, enrollment_id)
    if os.path.isdir(enrollment_upload_dir):
        upload_files = os.listdir(enrollment_upload_dir)
    return render(request, 'crm/enrollment.html', locals())


@csrf_exempt
def enrollment_fileupload(request, enrollment_id):
    conf_dir = conf.settings.CRM_FILE_UPLOADS_DIR[0]
    enrollment_upload_dir = os.path.join(conf_dir, enrollment_id)
    if not os.path.isdir(enrollment_upload_dir):
        os.mkdir(enrollment_upload_dir)
    file_obj = request.FILES.get('file')
    new_file_dir = os.path.join(enrollment_upload_dir, file_obj.name)
    with open(new_file_dir, 'wb') as f:
        for chunks in file_obj.chunks():
            f.write(chunks)
    return HttpResponse(json.dumps({'status': True, }))
