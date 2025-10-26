"""
File: urls.py
Author: Anthony Xie
Email: xiea@bu.edu
Description: URL patterns for the Mini Insta application.
Maps URL patterns to view functions for profile-related pages.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public views (no login required)
    path('', views.ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/followers/', views.ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following/', views.ShowFollowingDetailView.as_view(), name='show_following'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),

    # Authentication views
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
    path('logout_confirmation/', views.LogoutConfirmationView.as_view(), name='logout_confirmation'),
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),

    # User-specific views (login required, no pk in URL)
    path('profile/', views.ShowUserProfileView.as_view(), name='show_user_profile'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('profile/create_post/', views.CreatePostView.as_view(), name='create_post'),
    path('profile/feed/', views.NewsFeedView.as_view(), name='news_feed'),
    path('profile/search/', views.SearchView.as_view(), name='search'),

    # Post management (login required)
    path('post/<int:pk>/update/', views.UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),

    # Social interactions (login required)
    path('profile/<int:pk>/follow/', views.CreateFollowView.as_view(), name='create_follow'),
    path('profile/<int:pk>/delete_follow/', views.DeleteFollowView.as_view(), name='delete_follow'),
    path('post/<int:pk>/comment/', views.CreateCommentView.as_view(), name='create_comment'),
    path('post/<int:pk>/like/', views.CreateLikeView.as_view(), name='create_like'),
    path('post/<int:pk>/delete_like/', views.DeleteLikeView.as_view(), name='delete_like'),
]
