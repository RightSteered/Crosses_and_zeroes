from django.forms import ModelForm
from .models import Post, Response
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm


class Newpost(ModelForm):
    class Meta:
        model = Post
        fields = (
            'category',
            'title',
            'text'
        )


class Respond(ModelForm):
    class Meta:
        model = Response
        fields = (
            'text',
        )

class CommonSignup(SignupForm):
    def save(self, request):
        user = super(CommonSignup, self).save(request)
        common_group = Group.objects.get(name='Active')
        common_group.user_set.add(user)
        return user