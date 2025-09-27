"""
File: models.py
Author: Anthony Xie
Email: xiea@bu.edu
Description: Data models for the Mini Insta application.
Contains the Profile model that represents user profiles.
"""

from django.db import models

class Profile(models.Model):
    """
    Model representing a user profile for the mini Instagram application.
    """
    username = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField(max_length=500)
    bio_text = models.TextField(max_length=500, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return string representation of the Profile.
        """
        return f"{self.username} ({self.display_name})"
