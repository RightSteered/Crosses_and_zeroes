from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


class Author(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Ник')
    user_rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commRat = self.user_name.comment_set.aggregate(commRating=Sum('commentRating'))
        cRat = 0
        cRat += commRat.get('commRating')

        self.user_rating = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.user_name}'


class Category(models.Model):
    cat_id = models.CharField(max_length=64, unique=True, verbose_name= 'Название категории')
    cat_sub = models.ManyToManyField(User, verbose_name='Подписчики', blank=True)

    def __str__(self):
        return f'{self.cat_id}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор', default='1')
    NEWS = 'NW'
    ARTICLE = 'ART'
    CATEGORY_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    ]
    cat_type = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default=ARTICLE)
    created = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, verbose_name='Категория', through='PostCategory')
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + "..."

    def showcat(self):
        if self.postCategory:
            return str([postCategory.cat_id for postCategory in self.postCategory.all()])


    def get_absolute_url(self):
        return f'/news/{self.id}'





class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentAuthor = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    commentDate = models.DateTimeField(auto_now_add=True)
    commentRating = models.SmallIntegerField(default=0)

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    catThrough = models.ForeignKey(Category, on_delete=models.CASCADE)









