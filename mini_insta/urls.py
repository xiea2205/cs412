"""
File: urls.py
Author: Anthony Xie
Email: xiea@bu.edu
Description: URL patterns for the Mini Insta application.
Maps URL patterns to view functions for profile-related pages.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/', views.CreatePostView.as_view(), name='create_post'),
]