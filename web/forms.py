from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Enter a valid email")
    first_name = forms.CharField(max_length=200, help_text="Enter your first name")
    last_name = forms.CharField(max_length=200, help_text="Enter your last name")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')