from django import template
import os

register = template.Library()


@register.filter(name='Censor')
def censor(word):
    with open('bad_words.txt') as f:
        for word in f:
            if word:
                word = '(CENSORED)'
    return word
