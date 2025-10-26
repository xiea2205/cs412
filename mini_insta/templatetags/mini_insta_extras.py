"""
File: mini_insta_extras.py
Author: Anthony Xie
Email: xiea@bu.edu
Description: Custom template tags and filters for Mini Insta.
"""

from django import template
from mini_insta.models import Follow

register = template.Library()

@register.filter(name='is_following')
def is_following(follower_profile, target_profile):
    """
    Template filter to check if follower_profile is following target_profile.

    Parameters:
        follower_profile: The Profile that might be following.
        target_profile: The Profile being followed.

    Returns:
        bool: True if follower_profile is following target_profile.
    """
    if not follower_profile or not target_profile:
        return False
    return Follow.is_following(follower_profile, target_profile)


@register.filter(name='call')
def call_method(obj, arg):
    """
    Template filter to call a method on an object with a single argument.

    Parameters:
        obj: The object to call the method on.
        arg: The argument to pass to the method.

    Returns:
        The result of calling the method.
    """
    if callable(obj):
        return obj(arg)
    return None
