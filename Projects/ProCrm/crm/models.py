from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UseProfile(models.Model):
    """
    用户表
    """
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(unique=True, max_length=32)
    menus = models.ManyToManyField("Menu")

    def __str__(self):
        return self.name


class Menu(models.Model):
    """
    动态菜单
    """
    name = models.CharField(unique=True, max_length=32)
    url_type = models.SmallIntegerField(choices=((0, 'relative_name'), (1, 'absolute_url')))
    url_name = models.CharField(unique=True, max_length=128)

    def __str__(self):
        return self.name