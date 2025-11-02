"""
Name: Anthony Xie
Email: anthoxie@bu.edu
Description: Views for the voter_analytics application. Includes list view with filtering,
detail view, and graphs view with plotly visualizations.
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Voter
import plotly
import plotly.graph_objs as go
from collections import Counter


class VotersListView(ListView):
    """Display a list of voters with filtering and pagination."""
    model = Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        """Filter voters based on GET parameters."""
        queryset = Voter.objects.all()

        party = self.request.GET.get('party')
        min_birth_year = self.request.GET.get('min_birth_year')
        max_birth_year = self.request.GET.get('max_birth_year')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_birth_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_birth_year))
        if max_birth_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_birth_year))
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        if v20state:
            queryset = queryset.filter(v20state=True)
        if v21town:
            queryset = queryset.filter(v21town=True)
        if v21primary:
            queryset = queryset.filter(v21primary=True)
        if v22general:
            queryset = queryset.filter(v22general=True)
        if v23town:
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        """Add filter options to context."""
        context = super().get_context_data(**kwargs)

        parties = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        context['parties'] = parties
        context['birth_years'] = range(1920, 2010)
        context['voter_scores'] = range(6)

        context['current_party'] = self.request.GET.get('party', '')
        context['current_min_birth_year'] = self.request.GET.get('min_birth_year', '')
        context['current_max_birth_year'] = self.request.GET.get('max_birth_year', '')
        context['current_voter_score'] = self.request.GET.get('voter_score', '')
        context['current_v20state'] = self.request.GET.get('v20state', '')
        context['current_v21town'] = self.request.GET.get('v21town', '')
        context['current_v21primary'] = self.request.GET.get('v21primary', '')
        context['current_v22general'] = self.request.GET.get('v22general', '')
        context['current_v23town'] = self.request.GET.get('v23town', '')

        return context


class VoterDetailView(DetailView):
    """Display detailed information for a single voter."""
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


class GraphsView(TemplateView):
    """Display graphs showing voter statistics using Plotly."""
    template_name = 'voter_analytics/graphs.html'

    def get_context_data(self, **kwargs):
        """Override get_context_data to generate graphs based on filtered data."""
        context = super().get_context_data(**kwargs)

        # Get filtered queryset based on GET parameters
        queryset = Voter.objects.all()

        party = self.request.GET.get('party')
        min_birth_year = self.request.GET.get('min_birth_year')
        max_birth_year = self.request.GET.get('max_birth_year')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_birth_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_birth_year))
        if max_birth_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_birth_year))
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        if v20state:
            queryset = queryset.filter(v20state=True)
        if v21town:
            queryset = queryset.filter(v21town=True)
        if v21primary:
            queryset = queryset.filter(v21primary=True)
        if v22general:
            queryset = queryset.filter(v22general=True)
        if v23town:
            queryset = queryset.filter(v23town=True)

        voters = queryset

        # Graph 1: Histogram of voter distribution by birth year
        birth_years = [voter.date_of_birth.year for voter in voters]
        birth_year_counter = Counter(birth_years)
        years = sorted(birth_year_counter.keys())
        counts = [birth_year_counter[year] for year in years]

        fig1 = go.Figure(data=[go.Bar(x=years, y=counts)])
        fig1.update_layout(
            title='Voter Distribution by Birth Year',
            xaxis_title='Birth Year',
            yaxis_title='Number of Voters'
        )
        graph1_html = plotly.offline.plot(fig1, auto_open=False, output_type='div')

        # Graph 2: Pie chart of distribution by party affiliation
        party_affiliations = [voter.party_affiliation for voter in voters]
        party_counter = Counter(party_affiliations)
        labels = list(party_counter.keys())
        values = list(party_counter.values())

        fig2 = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig2.update_layout(title='Distribution by Party Affiliation')
        graph2_html = plotly.offline.plot(fig2, auto_open=False, output_type='div')

        # Graph 3: Histogram of election participation counts
        elections = {
            'v20state': sum(1 for v in voters if v.v20state),
            'v21town': sum(1 for v in voters if v.v21town),
            'v21primary': sum(1 for v in voters if v.v21primary),
            'v22general': sum(1 for v in voters if v.v22general),
            'v23town': sum(1 for v in voters if v.v23town),
        }

        fig3 = go.Figure(data=[go.Bar(x=list(elections.keys()), y=list(elections.values()))])
        fig3.update_layout(
            title='Election Participation',
            xaxis_title='Election',
            yaxis_title='Number of Voters'
        )
        graph3_html = plotly.offline.plot(fig3, auto_open=False, output_type='div')

        # Get filter options for context
        parties = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')

        # Add all data to context
        context['graph1'] = graph1_html
        context['graph2'] = graph2_html
        context['graph3'] = graph3_html
        context['parties'] = parties
        context['birth_years'] = range(1920, 2010)
        context['voter_scores'] = range(6)
        context['current_party'] = self.request.GET.get('party', '')
        context['current_min_birth_year'] = self.request.GET.get('min_birth_year', '')
        context['current_max_birth_year'] = self.request.GET.get('max_birth_year', '')
        context['current_voter_score'] = self.request.GET.get('voter_score', '')
        context['current_v20state'] = self.request.GET.get('v20state', '')
        context['current_v21town'] = self.request.GET.get('v21town', '')
        context['current_v21primary'] = self.request.GET.get('v21primary', '')
        context['current_v22general'] = self.request.GET.get('v22general', '')
        context['current_v23town'] = self.request.GET.get('v23town', '')

        return context
