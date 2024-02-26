from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """

    Form for creating and updating a post.

    """
    class Meta:
        model = Post
        fields = ('title', 'content', 'category', 'image')

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 255:
            raise forms.ValidationError('Title cannot exceed 255 characters.')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > 2048:
            raise forms.ValidationError('Content cannot exceed 2048 characters.')
        return content


class SearchForm(forms.Form):
    """

    Form for searching posts.

    """
    query = forms.CharField(max_length=100, required=False)


class CommentForm(forms.ModelForm):
    """

    Form for creating comments on posts.

    """
    comment_content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('comment_content',)
