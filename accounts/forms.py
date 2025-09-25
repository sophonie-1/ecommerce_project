from django.forms import ModelForm
from .models import Profile
from django import forms


class ProfileModelForm(ModelForm):
    class Meta:
        model= Profile
        fields ='__all__'
        exclude =['user']