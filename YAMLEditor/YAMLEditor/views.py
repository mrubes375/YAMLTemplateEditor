from django.shortcuts import render, HttpResponse, render_to_response
from django.contrib.auth import authenticate, login
from .yaml_config import get_yaml


def context_dict(request, context):
    con_dict = {'user': request.user, 'my_yaml': get_yaml()}
    fin_dict = con_dict.copy()
    fin_dict.update(context)
    return fin_dict

def c_render(request, page, context={}):
    return render(request, page, context=context_dict(request, context))

def c_render_to_response(template, request, status_code, context={}):
    response = render_to_response(template, context=context_dict(request, context))
    response.status_code = status_code
    return response
def index(request):
    return c_render(request, 'index.html')

def login(request):
    return c_render(request, 'login.html')

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response
    # return c_render_to_response('404.html', request, 404)


def handler500(request):
    # response = render_to_response('500.html', {},
    #                               context_instance=RequestContext(request))
    # response.status_code = 500
    return c_render_to_response('500.html', request, 500)
