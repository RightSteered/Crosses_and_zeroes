from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    nickname = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Ник")

    def __str__(self):
        return f'{self.nickname}'

class Category(models.Model):
    cat_id = models.CharField(max_length=64, unique=True, verbose_name='Название категории')

    def __str__(self):
        return f'{self.cat_id}'


class Post(models.Model):
    author = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="Автор")
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    category = models.ManyToManyField(Category, verbose_name="Категория", through='PostCategory')



class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    catThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст")
