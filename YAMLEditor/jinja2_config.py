from __future__ import absolute_import

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse

from jinja2 import Environment
from datetime import datetime

class MyFunctions:
    def __init__():
        self.func = True
    def strip(dt):
        return dt.strftime('%B %d, %Y %-I:%M:%S %p')
    def link_maker(pk):
        return '/update/' + str(pk)

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'date': MyFunctions.strip,
        'detail_link': MyFunctions.link_maker
    })
    return env
