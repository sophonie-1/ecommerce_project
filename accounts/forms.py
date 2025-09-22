from django.forms import ModelForm
from .models import Profile
from django import forms


class ProfileModelForm(ModelForm):
    class Meta:
        model= Profile
        fields =['address']
        widgets = {
               'address': forms.Textarea(attrs={'rows': 4}),
           }
    