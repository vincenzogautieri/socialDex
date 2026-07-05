from django import forms
from .models import Post

DISALLOWED_WORDS = ['hack']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if any(word in title.lower() for word in DISALLOWED_WORDS):
            raise forms.ValidationError('Word not allowed')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if any(word in content.lower() for word in DISALLOWED_WORDS):
            raise forms.ValidationError('Word not allowed')
        return content
