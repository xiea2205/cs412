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
    path('profile/<int:pk>/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('profile/<int:pk>/followers/', views.ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following/', views.ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/<int:pk>/follow/', views.CreateFollowView.as_view(), name='create_follow'),
    path('profile/<int:pk>/unfollow/', views.UnfollowView.as_view(), name='unfollow'),
    path('profile/<int:pk>/news_feed/', views.NewsFeedView.as_view(), name='news_feed'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/', views.CreatePostView.as_view(), name='create_post'),
    path('post/<int:pk>/update/', views.UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/comment/', views.CreateCommentView.as_view(), name='create_comment'),
    path('post/<int:pk>/like/', views.CreateLikeView.as_view(), name='create_like'),
    path('post/<int:pk>/unlike/', views.UnlikeView.as_view(), name='unlike'),
]