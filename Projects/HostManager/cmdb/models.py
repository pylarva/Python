from django.db import models

# Create your models here.


class BusinessLine(models.Model):
    name = models.CharField(max_length=32, null=True)


class HostStatus(models.Model):
    status = models.CharField(max_length=10)


class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)


class HostDatabase(models.Model):
    name = models.CharField(max_length=32)
    ip = models.CharField(max_length=32)
    business = models.ForeignKey('BusinessLine', to_field='id', default=1)
    status = models.ForeignKey('HostStatus', to_field='id', default=2)
    idc_name = models.CharField(max_length=32)
    idc_cabinet = models.CharField(max_length=32)
    person = models.CharField(max_length=32)
    ctime = models.DateTimeField(auto_now_add=True)


class AppDatabase(models.Model):
    name = models.CharField(max_length=32)
    r = models.ManyToManyField('HostDatabase')


# class HostToApp(models.Model):
#     host_obj = models.ForeignKey(to='HostDatabase', to_field='id')
#     app_obj = models.ForeignKey(to='AppDatabase', to_field='id')


