"""
Name: Anthony Xie
Email: anthoxie@bu.edu
Description: URL patterns for the voter_analytics application.
"""

from django.urls import path
from .views import VotersListView, VoterDetailView, GraphsView

urlpatterns = [
    path('', VotersListView.as_view(), name='voters'),
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
    path('graphs', GraphsView.as_view(), name='graphs'),
]
