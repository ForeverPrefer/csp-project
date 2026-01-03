from django.db import models
from django.conf import settings

class Resource(models.Model):
    # 资源分类枚举
    RESOURCE_TYPES = (
        ('文档资料', '文档资料'),
        ('软件工具', '软件工具'),
        ('学习教程', '学习教程'),
        ('模板资源', '模板资源'),
    )
    
    resource_name = models.CharField(max_length=200, verbose_name="资源名称")
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES, verbose_name="资源分类")
    resource_file = models.FileField(upload_to='resources/%Y/%m/%d/', verbose_name="资源文件")
    resource_desc = models.TextField(blank=True, null=True, verbose_name="资源描述")
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="上传者")
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
    download_count = models.IntegerField(default=0, verbose_name="下载次数")

    class Meta:
        verbose_name = "资源"
        verbose_name_plural = "资源"
        ordering = ['-upload_time']

    def __str__(self):
        return self.resource_name