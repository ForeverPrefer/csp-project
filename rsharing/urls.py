from django.urls import path
from . import views

app_name = 'rsharing'

urlpatterns = [
    path('list/<str:resource_type>/', views.resource_list, name='resource_list'),
    path('download/<int:resource_id>/', views.download_resource, name='download'),
    path('detail/<int:resource_id>/', views.resource_detail, name='resource_detail'), 
    path('resource/<int:resource_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
]