from django.urls import path
from . import views

app_name = 'self'

urlpatterns = [
    path('wdzy/', views.wdzy, name='wdzy'),  
    path('wdxz/', views.wdxz, name='wdxz'), 
    path('sc/', views.sc, name='sc'), 
    path('sz/', views.sz, name='sz'), 
]