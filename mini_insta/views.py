"""
File: views.py
Author: Anthony Xie
Email: xiea@bu.edu
Description: View functions and classes for the Mini Insta application.
Contains views for displaying profile lists and individual profiles.
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import Profile, Post, Photo
from .forms import UpdateProfileForm, UpdatePostForm

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

        # Get uploaded image files
        image_files = self.request.FILES.getlist('image_files')

        # Create Photo objects for each uploaded file
        for image_file in image_files:
            Photo.objects.create(
                post=self.object,
                image_file=image_file
            )

        return response

class UpdateProfileView(UpdateView):
    """
    View to update a profile.
    """
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'
    context_object_name = 'profile'

    def get_success_url(self):
        """
        Redirect to the profile page after updating.
        """
        return reverse('profile', kwargs={'pk': self.object.pk})

class UpdatePostView(UpdateView):
    """
    View to update a post's caption.
    """
    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'
    context_object_name = 'post'

    def get_success_url(self):
        """
        Redirect to the post detail page after updating.
        """
        return reverse('post_detail', kwargs={'pk': self.object.pk})

class DeletePostView(DeleteView):
    """
    View to delete a post.
    """
    model = Post
    template_name = 'mini_insta/delete_post.html'
    context_object_name = 'post'

    def get_success_url(self):
        """
        Redirect to the profile page after deleting.
        """
        return reverse('profile', kwargs={'pk': self.object.profile.pk})
