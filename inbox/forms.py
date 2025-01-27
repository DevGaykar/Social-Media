from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import InboxMesssage, Conversation

class InboxNewMessageForm(ModelForm):
    class Meta:
        model = InboxMesssage
        fields = ['body']
        labels = {
            'body': '',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add message...'})
        }

class GroupConversationForm(ModelForm):
    group_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'group-image-input',
            'accept': 'image/*'
        })
    )
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Participants'
    )

    class Meta:
        model = Conversation
        fields = ['group_name', 'group_image', 'participants']
        labels = {
            'group_name': 'Group Name',
            'group_image': 'Group Image',
        }
        widgets = {
            'group_name': forms.TextInput(attrs={'placeholder': 'Group Name', 'required': True}),
        }