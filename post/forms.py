from django import forms
from post.models import Post,ReportPost

class NewPostForm(forms.ModelForm):
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Caption'}),required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Tags | Seprate with comma'}),required=True)

    class Meta:
        model = Post
        fields = ['picture','caption','tags']

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption']
        labels = {
            'body':'',
            # 'tags':'Tags'
        }
        widgets ={
            'caption' : forms.TextInput(attrs={'class':'input','placeholder':'Caption'}),
            # 'tags' : forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Tags | Seprate with comma'})),
        }

class PostReportForm(forms.ModelForm):
    class Meta:
        model = ReportPost
        fields = ['body']
        labels = {
            'body':'Why are you reporting this post? ',
        # 'body':'',
        }
        widgets ={
            'body' : forms.TextInput(attrs={'class':'input','placeholder':'Reason '}),
        }
        
