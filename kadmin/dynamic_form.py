from django.forms import ModelForm
from crm import models


def create_dynamic_model_form(admin_class,form_add = False):
    """动态生产modelform表单"""
    """form_add 是用来判断修改还是添加页面，如果是添加页面则不执行admin_class.readonly_fields"""

    class Meta:
        model = admin_class.model  # 注意model 是固定变量，赋值时候不能做任何更改
        fields = '__all__'
        if form_add == False:
            exclude = admin_class.readonly_fields
            admin_class.form_add = False  #如果不写，admin_class实例都是传入的，并没有被实例化
        else:
            admin_class.form_add = True

    def __new__(cls, *args, **kwargs):      #自定义表单样式
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class': 'form-control'})
            # if field_name in admin_class.readonly_fields:
            #     field_obj.widget.attrs.update({'disabled': 'true'})
        return ModelForm.__new__(cls)

    dynamic_form = type('DynamicModelForm', (ModelForm,), {'Meta': Meta, '__new__': __new__})
    # print('dynamic_form:', dynamic_form)
    return dynamic_form
