from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

    def cleanTitle(self):
        title = self.cleaned_data.get('title')
        if 'hack' in title.lower():
            raise forms.ValidationError('Word not allowed')
        else:
            return title

    def cleanContent(self):
        content = self.cleaned_data.get('content')
        if 'hack' in content.lower():
            raise forms.ValidationError('Word not allowed')
        else:
            return content