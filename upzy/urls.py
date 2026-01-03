from django.urls import path
from . import views

app_name = 'upzy'

urlpatterns = [
    path('', views.upzy, name='upzy'),
]