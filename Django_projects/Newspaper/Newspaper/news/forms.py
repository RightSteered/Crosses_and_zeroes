from django.forms import ModelForm
from .models import Post

class Newpost(ModelForm):
    class Meta:
        model = Post
        fields = (
            'postCategory',
            'title',
            'text'
        )