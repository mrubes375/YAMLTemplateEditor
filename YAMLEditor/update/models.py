from django.db import models

# Create your models here.
class Change(models.Model):
    date = models.DateTimeField()
    files_changed = models.TextField()
    user = models.CharField(max_length=100)
    template = models.CharField(max_length=50)
    old_context = models.CharField(max_length=1000)
    new_context = models.CharField(max_length=1000)
