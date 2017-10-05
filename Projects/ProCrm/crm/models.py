from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    """
    用户表
    """
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    roles = models.ManyToManyField('Role', null=True, blank=True)

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
    url_icon = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Customer(models.Model):
    """
    客户信息表
    """
    name = models.CharField(max_length=32)
    qq = models.CharField(max_length=64, unique=True)
    weixin = models.CharField(max_length=64, blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    gender = models.PositiveIntegerField(choices=((0, 'Female'), (1, 'Male')), blank=True, null=True)
    phone = models.PositiveIntegerField(blank=True, null=True)

    source_choices = ((0, 'Baidu商桥'),
                      (1, '51CTO'),
                      (2, 'QQ群'),
                      (3, '知乎'),
                      (4, 'SOGO'),
                      (5, '转介绍'),
                      (6, '其他'),
                      )
    source = models.SmallIntegerField(choices=source_choices)
    referral_from = models.ForeignKey("Customer", related_name="my_referrals",
                                      blank=True, null=True, verbose_name="转介绍")

    consult_courses = models.ManyToManyField("Course")
    status_choices = ((0, '已报名'), (1, '未报名'), (2, '已退学'))
    status = models.SmallIntegerField(choices=status_choices)
    consultant = models.ForeignKey("UserProfile", verbose_name="课程顾问")
    consult_content = models.TextField(max_length=1024)

    graduated = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "客户信息表"


class Course(models.Model):
    """
    课程表
    """
    name = models.CharField(unique=True, max_length=64)
    price = models.PositiveIntegerField(default=19800)
    outline = models.TextField()

    def __str__(self):
        return self.name