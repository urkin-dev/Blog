from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from main_app.models import UserProfile

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UploadFileForm(forms.Form):
    username = forms.CharField(max_length=50)
    bio      = forms.CharField(max_length=170)
    file     = forms.FileField()