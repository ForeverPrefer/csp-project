from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = ['phone', 'email', 'display_name', 'real_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('个人信息', {'fields': ('display_name', 'real_name', 'email')}),
        ('权限', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'display_name', 'real_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    
    search_fields = ('phone', 'email', 'display_name', 'real_name')
    ordering = ('phone',)

admin.site.register(CustomUser, CustomUserAdmin)