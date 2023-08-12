from .models import Post
from django import forms


class BaseDetailUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = []


class DraftDetailUpdateForm(BaseDetailUpdateForm):
    pass


class PostDetailUpdateForm(BaseDetailUpdateForm):
    pass
