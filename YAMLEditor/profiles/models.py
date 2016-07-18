from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField()
    biography = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
