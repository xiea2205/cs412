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

    def get_absolute_url(self):
        """
        Return the URL to access this profile.
        """
        from django.urls import reverse
        return reverse('profile', kwargs={'pk': self.pk})

    def get_posts(self):
        """
        Return all posts for this profile, ordered by most recent first.
        """
        return self.posts.all().order_by('-timestamp')

    def get_followers(self):
        """
        Return a list of Profile objects who are following this profile.
        """
        # Get all Follow objects where this profile is being followed
        follow_objects = Follow.objects.filter(profile=self)
        # Return the follower profiles
        return [follow.follower_profile for follow in follow_objects]

    def get_num_followers(self):
        """
        Return the count of followers for this profile.
        """
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        """
        Return a list of Profile objects that this profile is following.
        """
        # Get all Follow objects where this profile is the follower
        follow_objects = Follow.objects.filter(follower_profile=self)
        # Return the followed profiles
        return [follow.profile for follow in follow_objects]

    def get_num_following(self):
        """
        Return the count of profiles this profile is following.
        """
        return Follow.objects.filter(follower_profile=self).count()


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

    def get_all_comments(self):
        """
        Return all comments for this post, ordered by most recent first.
        """
        return self.comments.all().order_by('-timestamp')

    def get_likes(self):
        """
        Return the count of likes for this post.
        """
        return self.likes.count()


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


class Follow(models.Model):
    """
    Model representing a follow relationship between two profiles.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followed_by')
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'follower_profile')

    def __str__(self):
        """
        Return string representation of the Follow relationship.
        """
        return f"{self.follower_profile.username} follows {self.profile.username}"


class Comment(models.Model):
    """
    Model representing a comment on a post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=500)

    def __str__(self):
        """
        Return string representation of the Comment.
        """
        return f"Comment by {self.profile.username} on {self.post}"


class Like(models.Model):
    """
    Model representing a like on a post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'profile')

    def __str__(self):
        """
        Return string representation of the Like.
        """
        return f"{self.profile.username} likes {self.post}"
