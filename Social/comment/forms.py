from django.forms import ModelForm
from django import forms
from .models import *

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields  = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder':'Add comment ...','style': 'background: var(--color-light);' })
        }
        labels = {
            'body' : ''
        }   

class ReplyCreateForm(ModelForm):
        class Meta:
            model = Reply
            fields  = ['body']
            widgets = {
                'body': forms.TextInput(attrs={'placeholder':'Add reply ...', 'class': '!text-sm',
                                                      'style': 'background: var(--color-light);'})
        }
            labels = {
                'body' : ''
        } 
        