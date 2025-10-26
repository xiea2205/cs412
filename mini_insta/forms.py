"""
File: forms.py
Author: Anthony Xie
Email: xiea@bu.edu
Description: Form classes for the Mini Insta application.
"""

from django import forms
from .models import Profile, Post

class CreateProfileForm(forms.ModelForm):
    """
    Form for creating a new profile.
    Does not include the User field - that is assigned programmatically.
    """
    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'profile_image_url', 'bio_text']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username (unique)'
            }),
            'display_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your display name'
            }),
            'profile_image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter profile image URL'
            }),
            'bio_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself',
                'rows': 4
            }),
        }

class UpdateProfileForm(forms.ModelForm):
    """
    Form for updating profile information.
    """
    class Meta:
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']
        widgets = {
            'display_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your display name'
            }),
            'profile_image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter profile image URL'
            }),
            'bio_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself',
                'rows': 4
            }),
        }

class UpdatePostForm(forms.ModelForm):
    """
    Form for updating post caption.
    """
    class Meta:
        model = Post
        fields = ['caption']
        widgets = {
            'caption': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter caption',
                'rows': 4
            }),
        }
