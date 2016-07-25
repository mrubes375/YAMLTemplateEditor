"""YAMLEditor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include, handler404, handler500
from django.contrib import admin
from rest_framework import routers
from .views import index, no_access, UserViewSet, register
from update.views import ChangeViewSet
import update.urls

router = routers.DefaultRouter()
router.register(r'change', ChangeViewSet)
router.register(r'user', UserViewSet)
handler404 = 'YAMLEditor.views.not_found'
handler500 = 'YAMLEditor.views.server_error'

urlpatterns = [
    url(r'^$', index),
    url(r'^register/$', register, name='register'),
    url(r'^admin/', admin.site.urls),
    url(r'^update/', include(update.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^no_access/$', no_access),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'})
]
