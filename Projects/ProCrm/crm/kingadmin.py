from django.contrib import admin
from crm import models
from kingadmin.base_admin import site, BaseAdmin

# Register your models here.


class CustomerAdmin(BaseAdmin):
    """
    自定义显示列
    """
    list_display = ('id', 'name', 'qq', 'consultant', 'source', 'consult_content', 'status', 'date')
    list_filter = ('source', 'status', 'consultant')
    list_per_page = 2
    search_fields = ('name', 'qq', 'status')
    readonly_fields = ('qq', 'name')
    actions = ["change_status", ]

    def change_status(self, request, querysets):
        querysets.update(status=1)

    change_status.short_description = "改变报名状态"


class CourseAdmin(BaseAdmin):
    list_display = ('id', 'name', 'price', 'outline')
    # list_filter = ('name',)
    # search_fields = ('name',)
    list_per_page = 2


site.register(models.Customer, CustomerAdmin)
site.register(models.Course, CourseAdmin)
