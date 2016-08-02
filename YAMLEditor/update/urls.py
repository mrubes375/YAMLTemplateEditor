from django.conf.urls import url, include
from .views import ChangeApp

urlpatterns = [
    url(r'^log/$', ChangeApp.log),
    url(r'^(?P<id>[0-9]+)/$', ChangeApp.log_details),
    url(r'^context/$', ChangeApp.ajax_context)

]
