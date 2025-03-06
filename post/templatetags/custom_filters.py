from django import template
from ..models import Follow

register = template.Library()

@register.filter
def mutual_friends_count(user, other_user):
    current_user_following = Follow.objects.filter(follower=user).values_list('following', flat=True)
    other_user_following = Follow.objects.filter(follower=other_user).values_list('following', flat=True)
    mutual_friends = set(current_user_following).intersection(set(other_user_following))
    return len(mutual_friends)