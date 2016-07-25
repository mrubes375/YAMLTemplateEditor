from django.forms import ModelForm, CharField, PasswordInput
from django.contrib.auth.models import User

class RegisterForm(ModelForm):
    password = CharField(widget=PasswordInput())
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
        ]
