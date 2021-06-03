from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Author, Post, Category, Comment
import datetime


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.now(tz=None)
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
