"""Newspaper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('news/', PostList.as_view()),
    path('authors/', AuthorList.as_view()),
    path('categories/', CatList.as_view()),
    path('categories/<int:pk>', CatView.as_view(), name='catview'),
    path('categories/subscribe/<int:pk>', Subscribe.as_view(), name='subscribe'),
    path('authors/<int:pk>', AuthorDesc.as_view()),
    path('news/<int:pk>', PostView.as_view()),
    path('news/add/', CreatePost.as_view()),
    path('news/edit/<int:pk>', EditPost.as_view(), name='newpost'),
    path('news/delete/<int:pk>', DeletePost.as_view(), name='delpost'),
    path('login/', TemplateView.as_view(), name='login'),
    path('', include('signup.urls')),
    path('', include('protect.urls')),
    path('sign/', include('signup.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/login', include('allauth.urls')),
    path('news/postslimit', include('django.contrib.flatpages.urls')),


]
