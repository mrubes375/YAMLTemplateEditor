from django.shortcuts import render, render_to_response
from tempfile import NamedTemporaryFile
from YAMLEditor.handle import DataBindingDOM, nested_temp_file_extender
from YAMLEditor.yaml_config import get_yaml
import os


def context_dict(request, context, function=get_yaml):
    con_dict = {'user': request.user, 'my_yaml': get_yaml()}
    fin_dict = con_dict.copy()
    fin_dict.update(context)
    return fin_dict

def render_with_yaml(request, page, context={}):
    context=context_dict(request, context)
    if request.user.is_staff:
        template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
        html = DataBindingDOM(template_dir, page).bind()
        temp_files = nested_temp_file_extender(html)
        file_name = temp_files[0]
    else:
        file_name = page
    return render(request, file_name, context)

def c_render_to_response(template, request, status_code, context={}):
    response = render_to_response(template, context=context_dict(request, context))
    response.status_code = status_code
    return response
