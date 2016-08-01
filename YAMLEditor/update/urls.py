from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^log/$', log),
    url(r'^(?P<id>[0-9]+)/$', log_details),
    url(r'^context/$', ajax_context)

]
