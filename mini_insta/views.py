"""
File: views.py
Author: Anthony Xie
Email: xiea@bu.edu
Description: View functions and classes for the Mini Insta application.
Contains views for displaying profile lists and individual profiles.
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from .models import Profile, Post, Photo

class ProfileListView(ListView):
    """
    View to display all profiles.
    """
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    """
    View to display a single profile.
    """
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

class PostDetailView(DetailView):
    """
    View to display a single post with all its details.
    """
    model = Post
    template_name = 'mini_insta/post_detail.html'
    context_object_name = 'post'

class CreatePostView(CreateView):
    """
    View to create a new post.
    """
    model = Post
    fields = ['profile', 'caption']
    template_name = 'mini_insta/create_post_form.html'

    def get_success_url(self):
        """
        Redirect to the profile page after creating a post.
        """
        return reverse('profile', kwargs={'pk': self.object.profile.pk})

    def form_valid(self, form):
        """
        Process the form and save the post and photos.
        """
        # Save the post
        response = super().form_valid(form)

        # Get image URLs from the form data
        image_urls = self.request.POST.getlist('image_url')

        # Create Photo objects for each URL
        for url in image_urls:
            if url.strip():  # Only create if URL is not empty
                Photo.objects.create(
                    post=self.object,
                    image_url=url.strip()
                )

        return response
