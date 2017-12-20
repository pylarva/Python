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

            # 只读字段
            if field_name in admin_obj.readonly_fields:
                field_obj.widget.attrs['disabled'] = True

        return forms.ModelForm.__new__(cls)

    def default_clean(self):
        # 表单验证
        for field in admin_obj.readonly_fields:

            # self.instance 是Form表单从数据库中取到的所有字段值组成的类对象
            # print(self.instance.__dict__)
            # {'_state': <django.db.models.base.ModelState object at 0x1042bd4e0>, 'id': 1, 'name': '刘一',
            # 'qq': '123456', 'weixin': '1234577778', 'age': 22, 'gender': 1, 'phone': 111}

            # 反射取原数据库中该只读字段的值
            field_val_from_db = getattr(self.instance, field)

            # cleaned_data 是前端from表单传过来的修改过后的数据
            field_val = self.cleaned_data.get(field)
            if field_val_from_db == field_val:
                pass
            else:
                self.add_error(field, ' "%s" is a readonly field ,value should be "%s" ' % (field, field_val_from_db))

    dynamic_model_form = type("DynamicModelForm", (forms.ModelForm,), {"Meta": Meta})
    setattr(dynamic_model_form, "__new__", __new__)
    setattr(dynamic_model_form, "clean", default_clean)

    return dynamic_model_form