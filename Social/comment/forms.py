from django.forms import ModelForm
from django import forms
from .models import *

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields  = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder':'Add comment ...'})
        }
        labels = {
            'body' : ''
        }