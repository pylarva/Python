from django.contrib import admin
from crm import models

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    """
    自定义显示列
    """
    list_display = ('id', 'name', 'qq', 'consultant', 'source', 'consult_content', 'status', 'date')


admin.site.register(models.UserProfile)
admin.site.register(models.Role)
admin.site.register(models.Menu)
admin.site.register(models.Course)
admin.site.register(models.Customer, CustomerAdmin)
