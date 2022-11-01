from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)

from .models import Announcement

# Create your views here.

def check_staff_admin_status(user):
    if user.groups.filter(name='Staff').exists() or user.groups.filter(name='WebAdmin').exists():
        return True
    else:
        return False

class AnnouncementCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Announcement
    fields = ['title', 'description', 'viewPerms']

    def form_valid(self, form):
        form.instance.postedBy = self.request.user
        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        return check_staff_admin_status(user)
        

class AnnouncementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Announcement
    fields = ['title', 'description', 'viewPerms']

    def test_func(self):
        user = self.request.user
        return check_staff_admin_status(user)

class AnnouncementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Announcement
    success_url = '/'

    def test_func(self):
        user = self.request.user
        return check_staff_admin_status(user)

class AnnouncementDetailView(UserPassesTestMixin, DetailView):
    model = Announcement

    def test_func(self):
        user = self.request.user
        viewPerms = self.get_object().viewPerms
        if check_staff_admin_status(user):
            return True
        if viewPerms == 'public':
            return True
        elif viewPerms == 'volunteers' and user.groups.filter('Volunteer').exists():
            return True
        
        return False

class AnnouncementListView(ListView):
    model = Announcement
    context_object_name = 'announcements'
    ordering = ['dateCreated']
    paginate_by = 25

    def get_queryset(self):
        userGroups = self.request.user.groups.all()
        # 0=Unauthenticated, 1=Volunteer, 2=Staff/WebAdmin
        viewPerm = 0
        if 'WebAdmin' in userGroups or 'Staff' in userGroups:
            viewPerm = 2
        elif 'Volunteer' in userGroups:
            viewPerm = 1

        if viewPerm >= 2:
            results = Announcement.objects.all()
        elif viewPerm == 1:
            results = Announcement.objects.filter(Q(viewPerms = 'volunteers') | Q(viewPers = 'public'))
        else:
            results = Announcement.objects.filter(viewPerms='public')

        return results
