from django import template

register = template.Library()


@register.filter
def censor(word):
    with open("bad_words.txt", 'r') as f:
        f.readlines()
        return f
