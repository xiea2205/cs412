"""
File: views.py
Author: Anthony Xie
Email: xiea@bu.edu
Description: View functions and classes for the Mini Insta application.
Contains views for displaying profile lists and individual profiles.
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

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
