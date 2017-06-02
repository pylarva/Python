from django.contrib import admin
from repository import models
# admin.site.register(models.Asset)
# admin.site.register(models.Server)
# admin.site.register(models.NetworkDevice)
# admin.site.register(models.UserProfile)
# admin.site.register(models.UserGroup)
# admin.site.register(models.BusinessUnit)
# admin.site.register(models.IDC)
# admin.site.register(models.Tag)
# admin.site.register(models.Disk)
# admin.site.register(models.Memory)
# admin.site.register(models.NIC)
# admin.site.register(models.AssetRecord)
# admin.site.register(models.ErrorLog)

admin.site.register(models.PhysicalMachines)
admin.site.register(models.VirtualMachines)
admin.site.register(models.HostMachines)
admin.site.register(models.MachineType)
admin.site.register(models.Asset)
admin.site.register(models.BusinessOne)
admin.site.register(models.BusinessTwo)
admin.site.register(models.BusinessThree)
admin.site.register(models.AdminInfo)
admin.site.register(models.AuthInfo)
admin.site.register(models.ReleaseType)
admin.site.register(models.UserGroup)