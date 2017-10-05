from django.shortcuts import render

# 这里两次导入了 base_admin, 实际上实例化了两次adminsite, 但是只得到一个大字典registered_sites
from kingadmin import app_config
from kingadmin import base_admin


def app_index(request):
    return render(request, "kingadmin/app_index.html", {"site": base_admin.site})


def table_data_list(request, app_name, model_name):
    admin_obj = base_admin.site.registered_sites[app_name][model_name]
    admin_obj.queryset = admin_obj.model.objects.all()
    return render(request, "kingadmin/table_data_list.html", locals())