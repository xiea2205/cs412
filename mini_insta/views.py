"""
File: views.py
Author: Anthony Xie
Email: xiea@bu.edu
Description: View functions and classes for the Mini Insta application.
Contains views for displaying profile lists and individual profiles.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse
from .models import Profile, Post, Photo, Follow, Comment, Like
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


class ShowFollowersDetailView(DetailView):
    """
    View to display all followers of a profile.
    """
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'


class ShowFollowingDetailView(DetailView):
    """
    View to display all profiles that a profile is following.
    """
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'


class CreateFollowView(View):
    """
    View to create a follow relationship.
    """
    def post(self, request, pk):
        """
        Handle POST request to follow a profile.
        """
        profile_to_follow = get_object_or_404(Profile, pk=pk)
        follower_profile_pk = request.POST.get('follower_profile_pk')
        follower_profile = get_object_or_404(Profile, pk=follower_profile_pk)

        # Create follow relationship if it doesn't exist
        Follow.objects.get_or_create(
            profile=profile_to_follow,
            follower_profile=follower_profile
        )

        return redirect('profile', pk=pk)


class UnfollowView(View):
    """
    View to remove a follow relationship.
    """
    def post(self, request, pk):
        """
        Handle POST request to unfollow a profile.
        """
        profile_to_unfollow = get_object_or_404(Profile, pk=pk)
        follower_profile_pk = request.POST.get('follower_profile_pk')
        follower_profile = get_object_or_404(Profile, pk=follower_profile_pk)

        # Delete follow relationship if it exists
        Follow.objects.filter(
            profile=profile_to_unfollow,
            follower_profile=follower_profile
        ).delete()

        return redirect('profile', pk=pk)


class CreateCommentView(View):
    """
    View to create a comment on a post.
    """
    def post(self, request, pk):
        """
        Handle POST request to create a comment.
        """
        post = get_object_or_404(Post, pk=pk)
        profile_pk = request.POST.get('profile_pk')
        profile = get_object_or_404(Profile, pk=profile_pk)
        comment_text = request.POST.get('comment_text')

        if comment_text:
            Comment.objects.create(
                post=post,
                profile=profile,
                text=comment_text
            )

        return redirect('post_detail', pk=pk)


class CreateLikeView(View):
    """
    View to create a like on a post.
    """
    def post(self, request, pk):
        """
        Handle POST request to like a post.
        """
        post = get_object_or_404(Post, pk=pk)
        profile_pk = request.POST.get('profile_pk')
        profile = get_object_or_404(Profile, pk=profile_pk)

        # Create like if it doesn't exist
        Like.objects.get_or_create(
            post=post,
            profile=profile
        )

        return redirect('post_detail', pk=pk)


class UnlikeView(View):
    """
    View to remove a like from a post.
    """
    def post(self, request, pk):
        """
        Handle POST request to unlike a post.
        """
        post = get_object_or_404(Post, pk=pk)
        profile_pk = request.POST.get('profile_pk')
        profile = get_object_or_404(Profile, pk=profile_pk)

        # Delete like if it exists
        Like.objects.filter(
            post=post,
            profile=profile
        ).delete()

        return redirect('post_detail', pk=pk)


class NewsFeedView(DetailView):
    """
    View to display personalized news feed for a profile.
    """
    model = Profile
    template_name = 'mini_insta/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        """
        Add feed posts to context.
        """
        context = super().get_context_data(**kwargs)

        # Get profiles that this profile is following
        following_profiles = self.object.get_following()

        # Get all posts from followed profiles, ordered by most recent
        feed_posts = Post.objects.filter(
            profile__in=following_profiles
        ).order_by('-timestamp')

        context['feed_posts'] = feed_posts
        return context
