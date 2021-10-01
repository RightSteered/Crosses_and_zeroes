from django_filters import FilterSet, DateFilter, CharFilter, OrderingFilter
from .models import Post, Author
from django.forms import DateInput


class PostFilter(FilterSet):
    date = DateFilter(field_name='created',
                      widget=DateInput(attrs={'type': 'date'}),
                      lookup_expr='lt',
                      label='Начиная с даты:')
    title = CharFilter(field_name='title',
                       label='Название',
                       lookup_expr=['icontains'])

    class Meta:
        model = Post
        fields = (
            'title',
            'author',
            'postCategory',
            'date'
        )


