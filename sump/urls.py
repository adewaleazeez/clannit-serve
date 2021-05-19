"""sump URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
# This Imports are for serving media files
from django.conf import settings
from django.urls import re_path
from django.views.static import serve
from rest_framework import routers
from api.views import *
from rest_framework.documentation import include_docs_urls

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'visitor', VisitorViewSet)
router.register(r'user', UserViewSet)
router.register(r'role', RoleViewSet)
router.register(r'estate', EstateViewSet)
router.register(r'login', LoginUserViewSet, base_name='login')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('acc/', include('app.user.urls')),
    path('', include('app.site_mgt.urls')),
    path('accounts/', include('registration.backends.default.urls')),
    path('api/v1/docs', include_docs_urls(title='Sump Backend API', public=False)),
]

urlpatterns += [
    re_path(
        r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }

    ),
]