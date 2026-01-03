from django.db import models
from django.conf import settings

class DownloadHistory(models.Model):
    """下载历史记录模型"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    resource = models.ForeignKey('upzy.Resource', on_delete=models.CASCADE, verbose_name='资源')
    downloaded_at = models.DateTimeField(auto_now_add=True, verbose_name='下载时间')
    
    class Meta:
        verbose_name = '下载历史'
        verbose_name_plural = '下载历史'
        ordering = ['-downloaded_at']
    
    def __str__(self):
        return f"{self.user.display_name} 下载了 {self.resource.resource_name}"