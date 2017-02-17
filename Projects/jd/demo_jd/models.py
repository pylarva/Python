from django.db import models

# Create your models here.


class UserDatabase(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
