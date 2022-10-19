from django.forms import TextInput
from django.shortcuts import render
from django.core import serializers
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
from colorfield.widgets import ColorWidget

from .models import Event
from .serializers import EventSerializer
from .utilities import convertHexToRgb


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

class EventDetailView(UserPassesTestMixin, DetailView):
    model = Event

    def test_func(self):
        event = self.get_object()
        user = self.request.user
        if user.groups.filter(name='Staff').exists() or user.groups.filter(name='WebAdmin').exists():
            return True
        if event.viewPerms == 'public':
            return True
        elif event.viewPerms == 'volunteers' and user.groups.filter(name='Volunteer').exists():
            return True
        else:
            return False

class EventCreateView(LoginRequiredMixin, UserPassesTestMixin,CreateView):
    model = Event
    fields = ['title', 'startTime', 'endTime', 'description', 'viewPerms', 'color']

    def get_form(self):
        form = super().get_form()
        form.fields['startTime'].widget = TextInput(attrs={'type': 'datetime-local'})
        form.fields['endTime'].widget = TextInput(attrs={'type': 'datetime-local'})
        form.fields['color'].widget = TextInput(attrs={'type': 'color'})
        return form

    def test_func(self):
        if self.request.user.has_perm('can_edit_events'):
            return True
        else:
            return False

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['title', 'startTime', 'endTime', 'description', 'viewPerms', 'color']

    def get_form(self):
        form = super().get_form()
        form.fields['startTime'].widget = TextInput(attrs={'type': 'datetime-local'})
        form.fields['endTime'].widget = TextInput(attrs={'type': 'datetime-local'})
        form.fields['color'].widget = TextInput(attrs={'type': 'color'})
        return form

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
        user = self.request.user
        context = super().get_context_data(**kwargs)
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        daysInMonth = calendar.monthrange(year, month)[1]
        monthStart = timezone.make_aware(datetime.datetime(year, month, 1))
        monthEnd = timezone.make_aware(datetime.datetime(year, month, daysInMonth))
        if user.groups.filter(name='Staff').exists() or user.groups.filter(name='WebAdmin').exists():
            query = Event.objects.filter(Q(startTime__gte=monthStart) | Q(endTime__gte=monthStart)).filter(Q(startTime__lte=monthEnd) | Q(endTime__lte=monthEnd))
        elif user.groups.filter(name='Volunteer').exists():
            query = Event.objects.filter(Q(startTime__gte=monthStart) | Q(endTime__gte=monthStart)).filter(Q(startTime__lte=monthEnd) | Q(endTime__lte=monthEnd)).filter(Q(viewPerms='volunteers') | Q(viewPerms='public'))
        else:
            query = Event.objects.filter(Q(startTime__gte=monthStart) | Q(endTime__gte=monthStart)).filter(Q(startTime__lte=monthEnd) | Q(endTime__lte=monthEnd)).filter(Q(viewPerms='public'))
        eventsJson = []
        for item in query:
            itemDict = {'title': item.title, 'slug': item.slug, 'startTime': item.startTime, 'endTime': item.endTime, 'description': item.description,'color': item.color, 'rgbaColor': convertHexToRgb(item.color, 0.15)}
            eventsJson.append(itemDict)

        context['calYear'] = year
        context['calMonth'] = month
        context['monthName'] = months[month - 1]
        context['eventsJson'] = eventsJson
        return context