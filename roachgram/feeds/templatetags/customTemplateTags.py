from django import template
from ..models import Like , Bookmark
from users.models import FollowUser
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.simple_tag
def liked(user , post):
    return True if Like.objects.filter(post=post , user=user).exists() else False

@register.simple_tag
def bookmarked(user , post):
    return True if Bookmark.objects.filter(post=post , user=user).exists() else False


@register.filter
@stringfilter
def upto(value, delimiter=None):
    return value.split(delimiter)[0]
upto.is_safe = True


@register.simple_tag
def followedTheUser(follower , following):
    return True if FollowUser.objects.filter(follower=follower , following=following) else False


@register.simple_tag
def userSuggestion(user):
    likedByUser = Like.objects.filter(user=user)[0]
    otherUsers = Like.objects.filter(user__in=Like.objects.filter(post=likedByUser.post).values_list("user").exclude(user=user))[:2]

    return otherUsers
