from django.conf import settings
from django.db import models

from upzy.models import Resource

# 使用字符串引用避免循环导入
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'resource']
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
    
    def __str__(self):
        return f"{self.user.username} 收藏了 {self.resource.resource_name}"