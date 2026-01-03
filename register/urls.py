from django.urls import path
from . import views

app_name = 'register'

urlpatterns = [
    path('', views.register_view, name='register'),  # 注册和登录页面
    path('logout/', views.logout_view, name='logout'),  # 退出登录
]