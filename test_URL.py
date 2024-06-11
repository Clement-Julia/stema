"""
URL configuration for stema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Dans votre fichier urls.py

from django.contrib import admin
from django.urls import path
from django.conf.urls import handler404, handler500
from product.views import home, profile_view, handler404_view, handler500_view #,simulate_error

handler404 = handler404_view
handler500 = handler500_view

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('profile/', profile_view, name='profile'),  # Ajoutez une URL pour la vue de profil
    # path('simulate-error/', simulate_error, name='simulate_error'),  # URL pour provoquer une erreur 500
    # Autres URLs
]

