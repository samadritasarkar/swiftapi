from django import forms
from .models import Objects

class ObjectForm(forms.ModelForm):

    class Meta:
        model = Objects
        fields = ['name', 'file']
