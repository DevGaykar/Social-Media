from .models import Story
from django import forms

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['content']