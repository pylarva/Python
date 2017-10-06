from django import forms
from crm import models

# 自动生成类似这样的的ModelForm类
# class CustomerModelForm(forms.ModelForm):
#     class Meta:
#         model = models.Customer
#         fields = "__all__"


def CreateModelForm(request, admin_obj):
    """
    自动生成注册过的Model类
    :param request:
    :param admin_obj:
    :return:
    """
    class Meta:
        model = admin_obj.model
        fields = "__all__"

    def __new__(cls, *args, **kwargs):
        # 自动给FORM表单的所有的元素加样式
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
        return forms.ModelForm.__new__(cls)

    dynamic_model_form = type("DynamicModelForm", (forms.ModelForm,), {"Meta": Meta})
    setattr(dynamic_model_form, "__new__", __new__)

    return dynamic_model_form