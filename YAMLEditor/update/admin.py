from django.contrib import admin
from .models import Change
# Register your models here.

@admin.register(Change)
class ChangesRegister(admin.ModelAdmin):
    pass
