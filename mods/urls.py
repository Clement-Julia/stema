from django.contrib import admin
from django.urls import path, include
from . import views
from .proxy import proxy_view

urlpatterns = [
    path('', views.mod_list, name='mod_list'),
    path('view/<str:game_domain_name>/', views.view_mods, name='view_mods'),
    path('files/<str:game_domain_name>/<int:mod_id>/', views.get_files, name='get_files'),
    path('proxy/', proxy_view, name='proxy_view'),
]
