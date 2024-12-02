from django import forms

from .models import Comment, Post, User


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text', )


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author', )
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
