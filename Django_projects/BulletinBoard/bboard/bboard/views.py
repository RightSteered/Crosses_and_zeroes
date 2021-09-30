from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from .models import *
from .filters import PostFilter
from .forms import Newpost, Respond
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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
    model = Post
    template_name = 'post.html'
    context_object_name = 'posts'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.all()
        context['filter'] = Post.objects.filter(id=self.kwargs['pk'])
        context['comments'] = Response.objects.all()
        context['pcomm'] = Response.objects.filter(post=self.kwargs['pk'])
        return context


    def response_show(self, **kwargs):
        responses = Response.objects.filter(post=self.kwargs['pk']).order_by('-id')
        return responses


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = Newpost
    template_name = 'newpost.html'
    queryset = Post.objects.all()


class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'newpost.html'
    form_class = Newpost
    queryset = Post.objects.all()

    def get_post(self, **kwargs):
        post_id = self.kwargs.get('pk')
        return Post.objects.get(pk=post_id)


class CreateResponse(LoginRequiredMixin, CreateView):
    form_class = Respond
    template_name = 'respond.html'

    def create_response(self, request, args, **kwargs):
        context = super(CreateResponse, self).get_context_data(**kwargs)
        context['post'] = Post.objects.filter(id=self.kwargs['pk'])


