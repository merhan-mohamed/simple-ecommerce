from django import forms
from . import models
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']




class Profile(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields =['address','country', 'image']