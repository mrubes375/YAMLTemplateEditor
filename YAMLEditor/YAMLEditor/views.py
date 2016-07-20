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


def not_found(request):
    return c_render(request, '404.html')

def server_error(request):
    return c_render(request, '500.html')

def no_access(request):
    return c_render(request, 'no_access.html')
