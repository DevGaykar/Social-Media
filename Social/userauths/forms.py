from django import forms
from userauths.models import Profile
from django.contrib.auth.models import User


class EditProfileForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'First Name'}),required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'Last Name'}),required=True)
    bio = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'bio'}),required=True)
    url = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'Url'}),required=True)
    location = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'Location'}),required=True)

    class Meta:
        model = Profile
        fields = ['image','first_name','last_name','bio','url','location']
