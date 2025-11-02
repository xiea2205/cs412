"""
Name: Anthony Xie
Email: anthoxie@bu.edu
Description: Admin configuration for the voter_analytics application.
"""

from django.contrib import admin
from .models import Voter


class VoterAdmin(admin.ModelAdmin):
    """Admin configuration for Voter model."""
    list_display = ['first_name', 'last_name', 'street_number', 'street_name',
                    'date_of_birth', 'party_affiliation', 'voter_score']
    list_filter = ['party_affiliation', 'voter_score', 'precinct_number']
    search_fields = ['first_name', 'last_name', 'street_name']


admin.site.register(Voter, VoterAdmin)
