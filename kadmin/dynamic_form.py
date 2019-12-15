from django.forms import ModelForm


def create_dynamic_model_form(admin_class):
    """动态生产modelform表单"""
    class Meta:
        models = admin_class.model
        fields = '__all__'
    dynamic_form = type('DynamicModelForm', (ModelForm,), {'Meta': Meta})
    print('dynamic_form:',dynamic_form)