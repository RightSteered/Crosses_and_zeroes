from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Author, Post, Category, Comment
from django.core.paginator import Paginator
from .filters import PostFilter
import datetime
from .forms import Newpost


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


class PostView(DetailView):
    model = Post
    template_name = 'postread.html'
    context_object_name = 'post'


class AuthorList(ListView):
    model = Author
    template_name = 'authors.html'
    context_object_name = 'authors'
    queryset = Author.objects.all().order_by('-user_rating')


class AuthorDesc(DetailView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'author'


class CatList(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'


class Comments(DetailView):
    model = Comment
    context_object_name = 'comments'


class NewPost(ListView):
    model = Post
    template_name = 'newpost.html'

    def post(self, request, *args, **kwargs):

        title = request.POST['title']
        text = request.POST['text']

        newpost = Post(title = title, text=text)
        newpost.save()
        return super().get(request, *args, **kwargs)
