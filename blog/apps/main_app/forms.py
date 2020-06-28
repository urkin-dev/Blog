from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from main_app.models import UserProfile

class CreateUserForm(UserCreationForm):
    username = forms.CharField(error_messages={'required': 'Введите имя пользователя'})
    
    error_messages = {
        'password_mismatch': ("Пароли не совпадают"),
    }

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'username-edit'})
        }

class ProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        self.fields['bio'].required = False

    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'bio-edit', 'maxlength': '170', 'placeholder': 'Введите короткое описание'})
        }