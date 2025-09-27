"""
File: admin.py
Author: Anthony Xie
Email: xiea@bu.edu
Description: Django admin configuration for the Mini Insta application.
Registers models with the admin interface and customizes admin views.
"""

from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for Profile model.
    """
    list_display = ['username', 'display_name', 'join_date']
    list_filter = ['join_date']
    search_fields = ['username', 'display_name']
