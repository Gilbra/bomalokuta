"""
URL configuration for kabod project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import *

schema_view = get_schema_view(
   openapi.Info(
      title="API Kabod",
      default_version='v1',
      description="Docs Swagger pour l'API de différntes apps développées par Kabod ASBL",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('set_language/', set_language, name='set_language'),
    path('', home, name='home'),

    # Apps
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('bomalokuta/', include('bomalokuta.urls')),
    path('vax/', include('vax.urls')),
    path('terranova/', include('terranova.urls')),
    
    # Swagger UI
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Ajouter la gestion des fichiers statiques
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
