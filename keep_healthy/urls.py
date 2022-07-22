"""keep_healthy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path, include
from django.views.static import serve
from keep_healthy import settings
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'users/', include('users.urls')),
    path(r'diabetes/', include('diabetes.urls')),
    path(r'source/', include('source_data.urls')),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path('^static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS}, name='static')
]


from keep_healthy.settings import DEBUG

if DEBUG:
    import debug_toolbar
    urlpatterns.append(re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}))
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                      re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
                  ] + urlpatterns