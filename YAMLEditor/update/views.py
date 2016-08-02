from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from Render.render import render_with_yaml
from update.serializers import ChangeSerializer
from .models import Change
import os
from Render.decorators import admins_only
from rest_framework import viewsets
from YAMLEditor.handle import ChangeYAML, FileSearcher, GitCommitYaml
import json
from YAMLEditor.secrets import git_pass, git_username
from datetime import datetime

template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
class ChangeViewSet(viewsets.ModelViewSet):
    queryset = Change.objects.all().order_by('-date')
    serializer_class = ChangeSerializer

class ChangeApp:
    def ajax_context(request):
        if request.is_ajax():
            beg = datetime.now()
            data = json.loads(request.body.decode('utf-8'))
            tag = data['tag'].strip()
            new_context = data['new_context'].strip()
            update = ChangeYAML(tag, new_context).update()
            old_context = update[0]
            user = request.user
            search = FileSearcher()
            files_changed = ', '.join(search.get_files_changed(tag))
            commit = GitCommitYaml(git_username, git_pass, tag, update[1].encode())
            change = Change(files_changed=files_changed, user=user, template=tag, old_context=old_context, new_context=new_context)
            change.save()
            end = datetime.now()
            print(end-beg)
            return HttpResponse(data)
        else:
            return render_with_yaml(request, 'errors/404.html')



    @admins_only
    def log(request):
        changes = Change.objects.all().order_by('-date')
        return render_with_yaml(request, 'log.html', {'changes': changes})

    @admins_only
    def log_details(request, id):
        change = get_object_or_404(Change, pk=id)
        return render_with_yaml(request, 'log_details.html', {'change': change})
