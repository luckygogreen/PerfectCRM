from django.forms import ModelForm
from crm import models


class CustomerForm(ModelForm):
    class Meta:
        model = models.CustomerInfo
        # fields = '['name','cunsultant','source','status','phone','consult_course']'
        fields = '__all__'