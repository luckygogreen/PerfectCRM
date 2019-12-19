from django.forms import ModelForm
from crm import models


class CustomerForm(ModelForm):
    class Meta:
        model = models.CustomerInfo
        fields = ['name','cunsultant','address','source','referral_from','wechat_or_other','status','phone','consult_course']
        readonly_fields = ['cunsultant','status']
        # fields = '__all__'  #显示全部字段
        # exclude = ['consult_Details']  #排除要显示的字段，通常和fields = '__all__' 一起用

    def __new__(cls, *args, **kwargs):  #自定义表单样式
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class':'form-control'})
            if field_name in cls.Meta.readonly_fields:
                field_obj.widget.attrs.update({'disabled': 'true'})
        return ModelForm.__new__(cls)


