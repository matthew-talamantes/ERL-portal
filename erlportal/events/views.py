from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

import datetime
import calendar

from rest_framework import generics

from .models import Event
from .serializers import EventSerializer


# Create your views here.


class EventList(generics.ListCreateAPIView):
    """
        List all events, or create a new event
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        Retrieve, update or delete a event instance.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'slug'

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event

class EventCreateView(LoginRequiredMixin, UserPassesTestMixin,CreateView):
    model = Event
    fields = ['title', 'startTime', 'endTime', 'description', 'color']

    def test_func(self):
        if self.request.user.has_perm('can_edit_events'):
            return True
        else:
            return False

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['title', 'startTime', 'endTime', 'description', 'color']

    def test_func(self):
        if self.request.user.has_perm('can_edit_events'):
            return True
        else:
            return False

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = '/'

    def test_func(self):
        if self.request.user.has_perm('can_edit_events'):
            return True
        else:
            return False

class CalendarView(TemplateView):
    template_name = 'events/calendar.html'

    def get_context_data(self, **kwargs):
        months = ('January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
        context = super().get_context_data(**kwargs)
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        daysInMonth = calendar.monthrange(year, month)[1]
        monthStart = timezone.make_aware(datetime.datetime(year, month, 1))
        monthEnd = timezone.make_aware(datetime.datetime(year, month, daysInMonth))
        context['year'] = year
        context['month'] = month
        context['monthName'] = months[month - 1]
        context['events'] = Event.objects.filter(Q(startTime__gte=monthStart) | Q(endTime__gte=monthStart)).filter(Q(startTime__lte=monthEnd) | Q(endTime__lte=monthEnd))
        return context