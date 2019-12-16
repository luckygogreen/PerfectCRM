from django.forms import ModelForm
from crm import models


class CustomerForm(ModelForm):
    class Meta:
        model = models.CustomerInfo
        # fields = '['name','cunsultant','source','status','phone','consult_course']'
        fields = '__all__'

    # def __new__(cls, *args, **kwargs):
    #     for field_name in cls.base_fields:
    #         field_obj = cls.base_fields[field_name]
    #         field_obj.widget.attrs.update({'class':'form-control'})
    #     return ModelForm.__new__(cls)
