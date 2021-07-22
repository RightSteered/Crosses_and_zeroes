from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View, TemplateView
from .models import *
from django.core.paginator import Paginator
from .filters import PostFilter
import datetime
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-id')
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.now(tz=None)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

    @login_required()
    def new(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid:
            form.save()
        return super().get(request, *args, **kwargs)


class PostView(DetailView):
    template_name = 'postread.html'
    queryset = Post.objects.all()


class AuthorList(ListView):
    model = Author
    template_name = 'authors.html'
    context_object_name = 'authors'
    queryset = Author.objects.all().order_by('-user_rating')


class AuthorDesc(DetailView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'author'
    queryset = Author.objects.all()


class CatList(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.all().order_by('cat_id')


class CatView(ListView):
    model = PostCategory
    template_name = 'catview.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super(CatView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['filter'] = Category.objects.filter(id=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return Post.objects.filter(postCategory=self.kwargs['pk']).order_by('-created')


class Comments(DetailView):
    model = Comment
    context_object_name = 'comments'


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = Newpost
    template_name = 'newpost.html'
    queryset = Post.objects.all()




class EditPost(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'newpost.html'
    form_class = Newpost
    queryset = Post.objects.all()

    def get_post(self, **kwargs):
        post_id = self.kwargs.get('pk')
        return Post.objects.get(pk=post_id)


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'delpost.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class Subscribe(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        user = request.user
        category = get_object_or_404(Category, id=kwargs['pk'])
        if category.cat_sub.filter(username=request.user).exists():
            category.cat_sub.remove(user)
        else:
            category.cat_sub.add(user)

        return redirect(request.META['HTTP_REFERER'])









