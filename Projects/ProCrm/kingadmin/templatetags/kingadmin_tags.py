from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# 自定义前端显示列


@register.simple_tag
def get_app_name(model_obj):
    return model_obj._meta.app_label


@register.simple_tag
def get_modle_name(model_obj):
    return model_obj._meta.model_name


@register.simple_tag
def get_model_verbose_name(model_obj):
    model_name = model_obj._meta.verbose_name if model_obj._meta.verbose_name else model_obj._meta.verbose_name_plural

    if not model_name:
        model_name = model_obj._meta.model_name

    return model_name


@register.simple_tag
def build_table_row(admin_obj, obj):

    row_ele = ""
    if admin_obj.list_display:
        for index, column in enumerate(admin_obj.list_display):
            column_obj = obj._meta.get_field(column)

            if column_obj.choices:
                get_column_data = getattr(obj, "get_%s_display" % column)
                column_data = get_column_data()
            else:
                column_data = getattr(obj, column)
            if index == 0:
                td_ele = '''<td><a href="/kingadmin/{app_name}/{model_name}/{obj_id}/change/">{column_data}</a> </td>'''\
                            .format(app_name=admin_obj.model._meta.app_label,
                                    model_name=admin_obj.model._meta.model_name,
                                    obj_id=obj.id,column_data=column_data)
            else:
                td_ele = '''<td>%s</td>''' % column_data
            row_ele += td_ele
    else:
        row_ele += "<td>%s</td>" % obj
    return mark_safe(row_ele)
