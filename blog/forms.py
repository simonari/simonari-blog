from .models import Post
from django import forms


class DraftDetailUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = []
