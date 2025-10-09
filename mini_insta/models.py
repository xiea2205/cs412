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

    def get_posts(self):
        """
        Return all posts for this profile, ordered by most recent first.
        """
        return self.posts.all().order_by('-timestamp')


class Post(models.Model):
    """
    Model representing a post made by a profile.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return string representation of the Post.
        """
        return f"Post by {self.profile.username} at {self.timestamp}"

    def get_photos(self):
        """
        Return all photos associated with this post.
        """
        return self.photos.all()


class Photo(models.Model):
    """
    Model representing a photo attached to a post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos')
    image_url = models.URLField(max_length=500, blank=True)
    image_file = models.ImageField(upload_to='photos/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_image_url(self):
        """
        Return the URL for the image, prioritizing uploaded file over URL.
        """
        if self.image_file:
            return self.image_file.url
        return self.image_url

    def __str__(self):
        """
        Return string representation of the Photo.
        """
        return f"Photo for {self.post} at {self.timestamp}"
