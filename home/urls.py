from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.home, name="home"),
    path('logout/', views.logout1, name='logout'),
    path('search/suggest/', views.search_suggestions, name='search_suggestions'),
]