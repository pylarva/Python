from django.contrib import admin
from crm import models

# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.Role)
admin.site.register(models.Menu)
