from django import template
from ..models import Like , Bookmark

register = template.Library()

@register.simple_tag
def liked(user , post):
    return True if Like.objects.filter(post=post , user=user).exists() else False

@register.simple_tag
def bookmarked(user , post):
    return True if Bookmark.objects.filter(post=post , user=user).exists() else False