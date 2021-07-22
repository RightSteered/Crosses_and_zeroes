from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post, User
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives



@receiver(post_save, sender=Post)
def new_post_notification(sender, instance, created, **kwargs):
    if created:
        @receiver(m2m_changed, sender=Post.postCategory.through)
        def get_category(sender, instance, **kwargs):
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

@receiver(post_save, sender=User)
def greeting(sender, instance, created, **kwargs):
    if created:
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







