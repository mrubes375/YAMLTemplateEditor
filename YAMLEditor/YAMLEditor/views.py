from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from .yaml_config import get_yaml



def c_render(request, page, context={}):
    con_dict = {'user': request.user, 'my_yaml': get_yaml()}
    fin_dict = con_dict.copy()
    fin_dict.update(context)
    return render(request, page, context=fin_dict)

def index(request):
    return c_render(request, 'index.html')
    # return render(request, 'index.html', {'user': request.user, 'my_yaml': get_yaml(),})

def login(request):
    # username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(username=username, passwor=password)
    # if user is not None:
    #     if user.is_active:
    #         login(request, user)
    #         return index(request)
    #     else:
    #         return HttpResponse("Disabled Account")
    # else:
    #     return HttpResponse("Invalid Login")
    return c_render(request, 'login.html')
