from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post, User, Comment
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from .tasks import *


@receiver(post_save, sender=Post)
def new_post(sender, instance, created, **kwargs):
    if created:
        @receiver(m2m_changed, sender=Post.postCategory.through)
        def get_category(sender, instance, **kwargs):
            new_post_notification(instance)


@receiver(post_save, sender=User)
def greeting(sender, instance, created, **kwargs):
    if created:
        new_user_confirm(instance)


@receiver(post_save, sender=Comment)
def newcomment(sender, instance, created, **kwargs):
    if created:
        new_comment_notification(instance)
