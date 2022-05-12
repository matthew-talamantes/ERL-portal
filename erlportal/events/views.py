from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

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