from django.forms import ModelForm
from django import forms
from .models import InboxMesssage


class InboxNewMessageForm(ModelForm):
    class Meta:
        model = InboxMesssage
        fields = ['body']
        labels = {
            'body'  : '',
        }
        widgets = {
            'body':forms.Textarea(attrs={'rows' : 4,'placeholder':'Add message...'})
        }