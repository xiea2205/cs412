"""
File: create_sample_profiles.py
Author: Anthony Xie
Email: xiea@bu.edu
Description: Django management command to create sample Profile records.
Creates 5 sample profiles with realistic data for testing the Mini Insta application.
"""

from django.core.management.base import BaseCommand
from mini_insta.models import Profile

class Command(BaseCommand):
    help = 'Create sample profiles for testing'

    def handle(self, *args, **options):
        profiles_data = [
            {
                'username': 'alice_wonderland',
                'display_name': 'Alice Johnson',
                'profile_image_url': 'https://images.unsplash.com/photo-1494790108755-2616b332b0db?w=400&h=400&fit=crop&crop=faces',
                'bio_text': 'Adventure seeker and coffee lover. Exploring the world one cup at a time. ☕✈️',
            },
            {
                'username': 'bob_photographer',
                'display_name': 'Robert Smith',
                'profile_image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=faces',
                'bio_text': 'Professional photographer capturing life\'s beautiful moments. 📸',
            },
            {
                'username': 'charlie_chef',
                'display_name': 'Charlie Brown',
                'profile_image_url': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=faces',
                'bio_text': 'Chef at downtown bistro. Food is my passion! 🍳👨‍🍳',
            },
            {
                'username': 'diana_artist',
                'display_name': 'Diana Prince',
                'profile_image_url': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=400&fit=crop&crop=faces',
                'bio_text': 'Digital artist and designer. Creating beauty through pixels and paint. 🎨',
            },
            {
                'username': 'erik_coder',
                'display_name': 'Erik Müller',
                'profile_image_url': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop&crop=faces',
                'bio_text': 'Full-stack developer building the future, one line of code at a time. 💻',
            },
        ]

        # Loop through each profile data dictionary to create Profile objects
        for profile_data in profiles_data:
            # Get or create profile to avoid duplicates
            profile, created = Profile.objects.get_or_create(
                username=profile_data['username'],
                defaults=profile_data
            )
            # Check if the profile was newly created
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created profile: {profile.username}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Profile already exists: {profile.username}')
                )