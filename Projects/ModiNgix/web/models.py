from django.db import models

# Create your models here.


class NginxHost(models.Model):
    """
    Nginx主机地址 && 配置文件地址 && 重启命令
    """
    ip = models.CharField(max_length=32, null=True, blank=True)
    path = models.CharField(max_length=108, null=True, blank=True)
    reload_cmd = models.CharField(max_length=108, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Nginx主机节点"

    def __str__(self):
        return self.ip


class NginxLog(models.Model):
    """
    修改记录日志
    """
    ip = models.CharField(max_length=32, null=True, blank=True)
    record = models.CharField(max_length=108, null=True, blank=True)
    ctime = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "修改日志表"

    def __str__(self):
        return self.ip