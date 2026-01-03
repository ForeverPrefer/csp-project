from django.urls import path
from . import views

app_name = 'flview'

urlpatterns = [
    path('new/', views.new, name='new'),
    path('down/', views.down, name='down'),
    path('xz/', views.xz, name='xz'),
]