from django.shortcuts import render
from django.db.models import Q, F
from django.views.generic import TemplateView
from django.utils import timezone

from announcements.models import Announcement
from events.models import Event
from shifts.models import ShiftInstance
# Create your views here.

def get_user_perms(user):
    groupObjs = list(user.groups.all())
    userGroups = [x.name for x in groupObjs]

    viewPerm = 0
    if 'WebAdmin' in userGroups or 'Staff' in userGroups:
        viewPerm = 2
    elif 'Volunteer' in userGroups:
        viewPerm = 1

    return viewPerm

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        viewPerm = get_user_perms(user)
        currentTime = timezone.now()
        if viewPerm >= 2:
            announcements = Announcement.objects.all()
            events = Event.objects.all()
            openShifts = ShiftInstance.objects.filter(Q(slots__gt=F('staffCount') + F('volCount')))
        elif viewPerm == 1:
            announcements = Announcement.objects.filter(Q(viewPerms='volunteers') | Q(viewPerms='public'))
            events = Event.objects.filter(Q(viewPerms='volunteers') | Q(viewPerms='public'))
            openShifts = ShiftInstance.objects.filter(Q(volSlots__gt=F('volCount')))
        else:
            announcements = Announcement.objects.filter(viewPerms='public')
            events = Event.objects.filter(viewPerms='public')
            openShifts = []

        context['announcements'] = announcements[:6]
        context['events'] = events.filter(Q(startTime__gte=currentTime) | Q(endTime__gte=currentTime))[:10]
        if openShifts:
            context['openShifts'] = openShifts.filter(Q(date__gte=currentTime.date()))[:10]
        else:
            context['openShifts'] = openShifts

        return context

        