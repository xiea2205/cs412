"""
File: admin.py
Author: Anthony Xie
Email: xiea@bu.edu
Description: Django admin configuration for the Mini Insta application.
Registers models with the admin interface and customizes admin views.
"""

from django.contrib import admin
from .models import Profile, Post, Photo, Follow, Comment, Like

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for Profile model.
    """
    list_display = ['username', 'display_name', 'join_date']
    list_filter = ['join_date']
    search_fields = ['username', 'display_name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for Post model.
    """
    list_display = ['profile', 'caption', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['caption', 'profile__username']


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """
    Admin configuration for Photo model.
    """
    list_display = ['post', 'timestamp']
    list_filter = ['timestamp']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Admin configuration for Follow model.
    """
    list_display = ['follower_profile', 'profile', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['follower_profile__username', 'profile__username']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Comment model.
    """
    list_display = ['profile', 'post', 'text', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['text', 'profile__username']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """
    Admin configuration for Like model.
    """
    list_display = ['profile', 'post', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['profile__username']
