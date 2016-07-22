from rest_framework import serializers
from .models import Change

class ChangeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Change
        fields = ('date', 'files_changed', 'user', 'template', 'old_context', 'new_context')
