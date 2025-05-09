from django import forms
from .models import Blog, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =['content', ]
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Type your comment here...'}),
        }
    def __init__(self, *args, **kwargs):
        self.blog = kwargs.pop('blog', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.blog:
            self.fields['content'].widget.attrs.update({'placeholder': 'Type your comment here...', 'class': 'form-control', 'rows': 4})
        else:
            self.fields['content'].widget.attrs.update({'placeholder': 'Please login to post comment', 'class': 'form-control', 'rows': 4, 'readonly': True})
            self.fields['content'].required = False

class ImagePostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['image_file',]

class VideoPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['videos_file',]

class IdeaPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['content',]