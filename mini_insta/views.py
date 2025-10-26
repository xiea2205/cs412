"""
File: views.py
Author: Anthony Xie
Email: xiea@bu.edu
Description: View functions and classes for the Mini Insta application.
Contains views for displaying profile lists and individual profiles.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import Profile, Post, Photo, Follow, Comment, Like
from .forms import CreateProfileForm, UpdateProfileForm, UpdatePostForm


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """
    Custom LoginRequiredMixin that provides additional features for authenticated users.
    """
    def get_login_url(self):
        """
        Return the URL to redirect to for login.

        Returns:
            str: The login URL for this application.
        """
        return reverse('login')

    def get_user_profile(self):
        """
        Get the profile of the currently logged-in user.

        Returns:
            Profile: The profile associated with the logged-in user, or None if not found.
        """
        if self.request.user.is_authenticated:
            try:
                return Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                return None
        return None


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

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the profile view.

        Parameters:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context dictionary with additional data.
        """
        context = super().get_context_data(**kwargs)

        # Add current user's profile if authenticated
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                context['user_profile'] = None
        else:
            context['user_profile'] = None

        return context


class ShowUserProfileView(CustomLoginRequiredMixin, DetailView):
    """
    View to display the logged-in user's own profile.
    """
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        """
        Get the profile of the currently logged-in user.

        Returns:
            Profile: The profile associated with the logged-in user.
        """
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Add the user's own profile to context.

        Parameters:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context dictionary with user profile data.
        """
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.object
        return context


class PostDetailView(DetailView):
    """
    View to display a single post with all its details.
    """
    model = Post
    template_name = 'mini_insta/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """
        Add user profile to context if authenticated.

        Parameters:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context dictionary with user profile data.
        """
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                context['user_profile'] = None
        else:
            context['user_profile'] = None

        return context


class CreatePostView(CustomLoginRequiredMixin, CreateView):
    """
    View to create a new post.
    """
    model = Post
    fields = ['caption']
    template_name = 'mini_insta/create_post_form.html'

    def get_success_url(self):
        """
        Redirect to the user's profile page after creating a post.

        Returns:
            str: URL to redirect to after successful post creation.
        """
        return reverse('show_user_profile')

    def form_valid(self, form):
        """
        Process the form and save the post and photos.

        Parameters:
            form: The validated form instance.

        Returns:
            HttpResponse: The response after successful form processing.
        """
        # Get the user's profile
        profile = Profile.objects.get(user=self.request.user)

        # Set the profile for the post
        form.instance.profile = profile

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


class UpdateProfileView(CustomLoginRequiredMixin, UpdateView):
    """
    View to update a profile.
    """
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'
    context_object_name = 'profile'

    def get_object(self):
        """
        Get the profile of the currently logged-in user.

        Returns:
            Profile: The profile to update.
        """
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self):
        """
        Redirect to the user's profile page after updating.

        Returns:
            str: URL to redirect to after successful update.
        """
        return reverse('show_user_profile')


class UpdatePostView(CustomLoginRequiredMixin, UpdateView):
    """
    View to update a post's caption.
    """
    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'
    context_object_name = 'post'

    def get_queryset(self):
        """
        Limit queryset to posts owned by the logged-in user.

        Returns:
            QuerySet: Posts belonging to the current user's profile.
        """
        profile = Profile.objects.get(user=self.request.user)
        return Post.objects.filter(profile=profile)

    def get_success_url(self):
        """
        Redirect to the post detail page after updating.

        Returns:
            str: URL to redirect to after successful update.
        """
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class DeletePostView(CustomLoginRequiredMixin, DeleteView):
    """
    View to delete a post.
    """
    model = Post
    template_name = 'mini_insta/delete_post.html'
    context_object_name = 'post'

    def get_queryset(self):
        """
        Limit queryset to posts owned by the logged-in user.

        Returns:
            QuerySet: Posts belonging to the current user's profile.
        """
        profile = Profile.objects.get(user=self.request.user)
        return Post.objects.filter(profile=profile)

    def get_success_url(self):
        """
        Redirect to the user's profile page after deleting.

        Returns:
            str: URL to redirect to after successful deletion.
        """
        return reverse('show_user_profile')


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


class CreateFollowView(CustomLoginRequiredMixin, View):
    """
    View to create a follow relationship.
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Handle the follow request.

        Parameters:
            request: The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: Redirect to the profile page.
        """
        profile_to_follow = get_object_or_404(Profile, pk=kwargs['pk'])
        follower_profile = Profile.objects.get(user=request.user)

        # Prevent users from following themselves
        if profile_to_follow != follower_profile:
            # Create follow relationship if it doesn't exist
            Follow.objects.get_or_create(
                profile=profile_to_follow,
                follower_profile=follower_profile
            )

        return redirect('profile', pk=kwargs['pk'])


class DeleteFollowView(CustomLoginRequiredMixin, View):
    """
    View to remove a follow relationship.
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Handle the unfollow request.

        Parameters:
            request: The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: Redirect to the profile page.
        """
        profile_to_unfollow = get_object_or_404(Profile, pk=kwargs['pk'])
        follower_profile = Profile.objects.get(user=request.user)

        # Delete follow relationship if it exists
        Follow.objects.filter(
            profile=profile_to_unfollow,
            follower_profile=follower_profile
        ).delete()

        return redirect('profile', pk=kwargs['pk'])


class CreateCommentView(CustomLoginRequiredMixin, View):
    """
    View to create a comment on a post.
    """
    def post(self, request, pk):
        """
        Handle POST request to create a comment.

        Parameters:
            request: The HTTP request.
            pk: The primary key of the post.

        Returns:
            HttpResponse: Redirect to the post detail page.
        """
        post = get_object_or_404(Post, pk=pk)
        profile = Profile.objects.get(user=request.user)
        comment_text = request.POST.get('comment_text')

        if comment_text:
            Comment.objects.create(
                post=post,
                profile=profile,
                text=comment_text
            )

        return redirect('post_detail', pk=pk)


class CreateLikeView(CustomLoginRequiredMixin, View):
    """
    View to create a like on a post.
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Handle the like request.

        Parameters:
            request: The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: Redirect to the post detail page.
        """
        post = get_object_or_404(Post, pk=kwargs['pk'])
        profile = Profile.objects.get(user=request.user)

        # Prevent users from liking their own posts
        if post.profile != profile:
            # Create like if it doesn't exist
            Like.objects.get_or_create(
                post=post,
                profile=profile
            )

        return redirect('post_detail', pk=kwargs['pk'])


class DeleteLikeView(CustomLoginRequiredMixin, View):
    """
    View to remove a like from a post.
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Handle the unlike request.

        Parameters:
            request: The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: Redirect to the post detail page.
        """
        post = get_object_or_404(Post, pk=kwargs['pk'])
        profile = Profile.objects.get(user=request.user)

        # Delete like if it exists
        Like.objects.filter(
            post=post,
            profile=profile
        ).delete()

        return redirect('post_detail', pk=kwargs['pk'])


class NewsFeedView(CustomLoginRequiredMixin, DetailView):
    """
    View to display personalized news feed for a profile.
    """
    model = Profile
    template_name = 'mini_insta/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        """
        Get the profile of the currently logged-in user.

        Returns:
            Profile: The profile for the news feed.
        """
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Add feed posts to context.

        Parameters:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context dictionary with feed posts.
        """
        context = super().get_context_data(**kwargs)

        # Get profiles that this profile is following
        following_profiles = self.object.get_following()

        # Get all posts from followed profiles AND the user's own posts
        feed_posts = Post.objects.filter(
            Q(profile__in=following_profiles) | Q(profile=self.object)
        ).order_by('-timestamp')

        context['feed_posts'] = feed_posts
        context['user_profile'] = self.object
        return context


class SearchView(CustomLoginRequiredMixin, ListView):
    """
    View to search for profiles by username or display name.
    """
    model = Profile
    template_name = 'mini_insta/search.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        """
        Filter profiles based on search query.

        Returns:
            QuerySet: Profiles matching the search criteria.
        """
        query = self.request.GET.get('q', '')

        if query:
            return Profile.objects.filter(
                Q(username__icontains=query) | Q(display_name__icontains=query)
            )
        return Profile.objects.none()

    def get_context_data(self, **kwargs):
        """
        Add search query to context.

        Parameters:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context dictionary with search query.
        """
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')

        # Add user profile
        try:
            context['user_profile'] = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            context['user_profile'] = None

        return context


class CreateProfileView(CreateView):
    """
    View to create a new profile along with a user account.
    """
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        """
        Add UserCreationForm to context.

        Parameters:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context dictionary with UserCreationForm.
        """
        context = super().get_context_data(**kwargs)

        # Add UserCreationForm if not already in context
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()

        return context

    def form_valid(self, form):
        """
        Process both the profile form and user creation form.

        Parameters:
            form: The validated CreateProfileForm.

        Returns:
            HttpResponse: The response after successful form processing.
        """
        # Reconstruct UserCreationForm from POST data
        user_form = UserCreationForm(self.request.POST)

        # Validate both forms
        if user_form.is_valid():
            # Save the User object
            user = user_form.save()

            # Attach the User to the Profile instance
            form.instance.user = user

            # Log the user in
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Delegate to superclass to save Profile
            return super().form_valid(form)
        else:
            # If user form is invalid, re-render with errors
            return self.form_invalid(form)

    def form_invalid(self, form):
        """
        Handle invalid form submission.

        Parameters:
            form: The invalid form.

        Returns:
            HttpResponse: The response with form errors.
        """
        # Reconstruct UserCreationForm to show errors
        user_form = UserCreationForm(self.request.POST)
        user_form.is_valid()  # Trigger validation to populate errors

        return self.render_to_response(
            self.get_context_data(form=form, user_form=user_form)
        )

    def get_success_url(self):
        """
        Redirect to the new profile page after creation.

        Returns:
            str: URL to redirect to after successful profile creation.
        """
        return reverse('show_user_profile')


class LogoutConfirmationView(TemplateView):
    """
    View to display logout confirmation page.
    """
    template_name = 'mini_insta/logged_out.html'
