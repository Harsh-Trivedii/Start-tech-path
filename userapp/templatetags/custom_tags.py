from django import template
from userapp.models import UserProfile

register = template.Library()

@register.filter(name='is_premium_user')
def is_premium_user(user):
    try:
        return user.userprofile.is_premium
    except UserProfile.DoesNotExist:
        return False