from django.contrib import admin
from .models import Resource

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['resource_name', 'resource_type', 'get_uploader_display_name', 'upload_time', 'download_count']
    list_filter = ['resource_type', 'upload_time']
    search_fields = ['resource_name', 'resource_desc']
    readonly_fields = ['upload_time', 'download_count']
    
    def get_uploader_display_name(self, obj):
        return obj.uploader.get_display_name()
    get_uploader_display_name.short_description = '上传者'
    
    fieldsets = [
        ('基本信息', {
            'fields': ['resource_name', 'resource_type', 'resource_file']
        }),
        ('详细信息', {
            'fields': ['resource_desc', 'uploader', 'upload_time', 'download_count'],
            'classes': ['collapse'] # 下面这些东西可能多，所以这几个是折叠的，点击可展开
        }),
    ]