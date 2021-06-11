from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
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


class CatList(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'


class Comments(DetailView):
    model = Comment
    context_object_name = 'comments'


class CreatePost(CreateView):
    form_class = Newpost
    template_name = 'newpost.html'
    queryset = Post.objects.all()


class EditPost(UpdateView):
    template_name = 'newpost.html'
    form_class = Newpost
    queryset = Post.objects.all()

    def get_post(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class DeletePost(DeleteView):
    template_name = 'delpost.html'
    queryset = Post.objects.all()
    success_url = '/news/'





# class DeletePost(DeleteView):

