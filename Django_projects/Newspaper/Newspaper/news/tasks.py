from celery import app, shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from .models import Post, User
import datetime

@shared_task
def new_post_notification(instance):
    for cat in instance.postCategory.all():
        for user in cat.cat_sub.all():
            html_content = render_to_string('Msgletter.html', {'instance': instance, 'user': user})
            e_mail = user.email
            msg = EmailMultiAlternatives(
                subject=instance.title,
                body=instance.text,
                to=[e_mail]
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()


@shared_task
def new_user_confirm(instance):
    html_content = render_to_string('greetletter.html', {'instance': instance})
    e_mail = instance.email
    msg = EmailMultiAlternatives(
        subject=f'Приветствуем, {instance.username}!',
        body='Вы успешно зарегистрировались на портале!',
        to=[e_mail]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    return redirect('/news/')


@shared_task
def weekly_broadcast():
    date = datetime.date.today() - datetime.timedelta(days=7)
    wposts = Post.objects.filter(created__gte=date)
    for inst in wposts:
        for cat in inst.postCategory.all():
            for user in cat.cat_sub.all():
                html_content = render_to_string('Msgweekly.html', {'inst': inst, 'user': user})
                e_mail = user.email
                msg = EmailMultiAlternatives(
                    subject=Post.title,
                    body=Post.text,
                    to=[e_mail]
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()
