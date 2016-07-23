from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Change(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    files_changed = models.TextField()
    user = models.ForeignKey(User, null=True, blank=False)
    template = models.CharField(max_length=50)
    old_context = models.CharField(max_length=1000)
    new_context = models.CharField(max_length=1000)
