from django.forms import ModelForm
from .models import Post, Author, Category
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class Newpost(ModelForm):
    class Meta:
        model = Post
        fields = (
            'postCategory',
            'title',
            'text'
        )


class CommonSignup(SignupForm):
    def save(self, request):
        user = super(CommonSignup, self).save(request)
        common_group = Group.objects.get(name='Common')
        common_group.user_set.add(user)
        return user
