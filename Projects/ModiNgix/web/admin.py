from django.contrib import admin

# Register your models here.

from web import models
admin.site.register(models.NginxHost)
admin.site.register(models.NginxLog)
