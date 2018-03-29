from django.db import models

# Create your models here.


class UserProfile(models.Model):
    """
    用户账户
    """
    username = models.CharField(max_length=108, unique=True)
    pwd = models.CharField(max_length=108, null=True, blank=True)
    user_cookies = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.username