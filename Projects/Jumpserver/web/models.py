from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class IDC(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Host(models.Model):
    """存储所有主机"""
    hostname = models.CharField(max_length=64)
    ip_addr = models.GenericIPAddressField(unique=True)
    port = models.PositiveSmallIntegerField(default=22)
    idc = models.ForeignKey("IDC")

    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.ip_addr


class HostGroup(models.Model):
    """主机组"""
    name = models.CharField(max_length=64, unique=True)
    bind_hosts = models.ManyToManyField("BindHost")

    def __str__(self):
        return self.name


class RemoteUser(models.Model):
    """存储远程用户名密码"""
    username = models.CharField(max_length=64)
    auth_type_choices = ((0, 'ssh/password'), (1, 'ssh/key'))
    auth_type = models.SmallIntegerField(choices=auth_type_choices, default=0)
    password = models.CharField(max_length=128, blank=True, null=True)

    #hosts = models.ManyToManyField("Host")

    def __str__(self):
        return "%s(%s)%s" % (self.username, self.get_auth_type_display(), self.password)

    class Meta:
        unique_together = ('username', 'auth_type', 'password')


class BindHost(models.Model):
    """绑定远程主机和远程用户的对应关系"""
    host = models.ForeignKey("Host")
    remote_user = models.ForeignKey("RemoteUser")

    def __str__(self):
        return "%s -> %s" % (self.host, self.remote_user)

    class Meta:
        unique_together = ("host", "remote_user")


class UserProfileManager(BaseUserManager):
    """自定制Django admin用户管理"""
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ PermissionsMixin 继承Django的权限管理 """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )

    bind_hosts = models.ManyToManyField("BindHost", blank=True)
    host_groups = models.ManyToManyField("HostGroup", blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True



