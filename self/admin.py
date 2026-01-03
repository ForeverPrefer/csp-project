from django.contrib import admin
from .models import DownloadHistory

@admin.register(DownloadHistory)
class DownloadHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'resource', 'downloaded_at']
    list_filter = ['downloaded_at', 'resource__resource_type']
    search_fields = ['user__display_name', 'resource__resource_name']
    date_hierarchy = 'downloaded_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'resource')