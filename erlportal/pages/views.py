from django.shortcuts import render
from django.db.models import Q
from django.views.generic import TemplateView

from announcements.models import Announcement

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
        if viewPerm >= 2:
            announcements = Announcement.objects.all()
        elif viewPerm == 1:
            announcements = Announcement.objects.filter(Q(viewPerms='volunteers') | Q(viewPerms='public'))
        else:
            announcements = Announcement.objects.filter(viewPerms='public')

        context['announcements'] = announcements[:6]

        return context

        