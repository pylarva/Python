from django.contrib import admin
from crm import models

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    """
    自定义显示列
    """
    list_display = ('id', 'name', 'qq', 'consultant', 'source', 'consult_content', 'status', 'date')
    readonly_fields = ('qq', 'name')

    actions = ["action_test", ]

    def action_test(self, request, querysets):
        # print("action test",*args,**kwargs)
        querysets.update(status=0)

    action_test.short_description = "测试"


admin.site.register(models.UserProfile)
admin.site.register(models.Role)
admin.site.register(models.Menu)
admin.site.register(models.Course)
admin.site.register(models.Customer, CustomerAdmin)
