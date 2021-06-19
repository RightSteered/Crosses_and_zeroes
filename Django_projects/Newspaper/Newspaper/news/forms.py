from django.forms import ModelForm
from .models import Post, Author
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class Newpost(ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'text'
        )

class Login(ModelForm):
    class Meta:
        model = Author
        fields = (

        )

class Registration(ModelForm):
    class Meta:
        model = Author
        fields = (
            'user_name',

        )

class CommonSignup(SignupForm):
    def save(self, request):
        user = super(CommonSignup, self).save(request)
        common_group = Group.objects.get(name='Common')
        common_group.user_set.add(user)
        return user