import json
from django.db.models import Q
from kingadmin import forms
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# 这里两次导入了 base_admin, 实际上实例化了两次adminsite, 但是只得到一个大字典registered_sites
from kingadmin import app_config
from kingadmin import base_admin


def app_index(request):
    return render(request, "kingadmin/app_index.html", {"site": base_admin.site})


def filter_querysets(request, queryset):
    """ 多条件过滤 """
    condtions = {}
    print(request.GET)
    for k, v in request.GET.items():
        if k in ("page", "_o", "_q"):
            continue
        if v:
            condtions[k] = v
    print(condtions)
    query_res = queryset.filter(**condtions)
    return query_res, condtions


def get_orderby(request,queryset):
    """ 排序 """
    order_by_key = request.GET.get("_o")
    if order_by_key != None:
        query_res = queryset.order_by(order_by_key)
    else:
        query_res = queryset.order_by("id")
    return query_res


def get_queryset_search_result(request, queryset, admin_obj):
    """ 搜索 """
    search_key = request.GET.get("_q", "")
    q_obj = Q()
    q_obj.connector = "OR"
    for column in admin_obj.search_fields:
        q_obj.children.append(("%s__contains" % column, search_key))
    res = queryset.filter(q_obj)
    return res


def table_data_list(request, app_name, model_name):
    admin_obj = base_admin.site.registered_sites[app_name][model_name]
    obj_list = admin_obj.model.objects.all()

    # 批量操作动作
    if request.method == "POST":
        action = request.POST.get("action_select")
        selected_ids = request.POST.get("selected_ids")
        selected_ids = json.loads(selected_ids)
        print("action:", selected_ids, action)
        selected_objs = admin_obj.model.objects.filter(id__in=selected_ids)

        action_func = getattr(admin_obj, action)
        action_func(request, selected_objs)

    # 进行多条件过滤完 过滤条件继续返回给前端
    queryset, condtions = filter_querysets(request, obj_list)
    admin_obj.filter_condtions = condtions

    # 搜索
    queryset = get_queryset_search_result(request, queryset, admin_obj)

    # 排序
    sorted_queryset = get_orderby(request, queryset)

    # 分页
    paginator = Paginator(sorted_queryset, admin_obj.list_per_page)
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    admin_obj.querysets = objs

    return render(request, "kingadmin/table_data_list.html", locals())


def table_change(request, app_name, model_name, obj_id):
    """
    编辑表格
    :param request:
    :param app_name:
    :param model_name:
    :param obj_id:
    :return:
    """
    admin_obj = base_admin.site.registered_sites[app_name][model_name]

    # 自动创建用于生成编辑表格的ModelForm类
    model_form = forms.CreateModelForm(request, admin_obj=admin_obj)

    obj = admin_obj.model.objects.get(id=obj_id)

    if request.method == "GET":
        # 填充ModelFrom表格数据
        obj_form = model_form(instance=obj)
    elif request.method == "POST":
        # 更新表格数据
        obj_form = model_form(instance=obj, data=request.POST)
        if obj_form.is_valid():
            obj_form.save()

    return render(request, "kingadmin/table_change.html", locals())


def table_add(request, app_name, model_name):
    """
    添加数据
    :param request:
    :param app_name:
    :param model_name:
    :return:
    """
    admin_obj = base_admin.site.registered_sites[app_name][model_name]
    model_form = forms.CreateModelForm(request,admin_obj=admin_obj)

    if request.method == "GET":
        obj_form = model_form()

    elif request.method == "POST":
        # Form添加数据
        obj_form = model_form(data=request.POST)
        if obj_form.is_valid():
            obj_form.save()
        if not obj_form.errors:
            return redirect("/kingadmin/%s/%s/" % (app_name, model_name))
    return render(request, "kingadmin/table_add.html", locals())
