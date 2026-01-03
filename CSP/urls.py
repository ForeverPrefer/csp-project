from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 

admin.site.site_header = 'CSP 校园资源分享平台' 
admin.site.site_title = 'CSP 校园资源分享平台'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('rsharing/', include('rsharing.urls')),
    path('upzy/', include('upzy.urls')),
    path('flview/', include('flview.urls')),
    path('self/', include('self.urls')),
    path('about/', include('about.urls')),
    path('register/', include('register.urls')),  # 登录注册页面
    path('help/', include('help.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)