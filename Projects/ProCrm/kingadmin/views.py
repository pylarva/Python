from django.db.models import Q
from django.shortcuts import render
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

    # 进行多条件过滤完 过滤条件继续返回给前端
    queryset, condtions = filter_querysets(request, obj_list)
    print(queryset, condtions)
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
