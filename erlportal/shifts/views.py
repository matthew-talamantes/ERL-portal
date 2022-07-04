from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.forms import TextInput

from .models import BaseShift

# Create your views here.
class BaseShiftListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = BaseShift
    context_object_name = 'shifts'
    ordering = ['name']
    paginate_by = 25

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='Staff').exists() or user.groups.filter(name='WebAdmin').exists():
            return True
        else:
            return False

class BaseShiftDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = BaseShift

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='Staff').exists() or user.groups.filter(name='WebAdmin').exists():
            return True
        else:
            return False

class BaseShiftCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = BaseShift
    fields = ['name', 'description', 'date', 'startTime', 'endTime', 'repeat', 'endRepeat', 'minSlots', 'staffSlots', 'volSlots', 'defaultStaff', 'defaultVols']

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = TextInput(attrs={'type': 'date'})
        form.fields['startTime'].widget = TextInput(attrs={'type': 'time'})
        form.fields['endTime'].widget = TextInput(attrs={'type': 'time'})
        form.fields['endRepeat'].widget = TextInput(attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='Staff').exists() or user.groups.filter(name='WebAdmin').exists():
            return True
        else:
            return False

class BaseShiftUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BaseShift
    fields = ['name', 'description', 'date', 'startTime', 'endTime', 'repeat', 'endRepeat', 'minSlots', 'staffSlots', 'volSlots', 'defaultStaff', 'defaultVols']

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = TextInput(attrs={'type': 'date'})
        form.fields['startTime'].widget = TextInput(attrs={'type': 'time'})
        form.fields['endTime'].widget = TextInput(attrs={'type': 'time'})
        form.fields['endRepeat'].widget = TextInput(attrs={'type': 'date'})
        return form

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='Staff').exists() or user.groups.filter(name='WebAdmin').exists():
            return True
        else:
            return False

class BaseShiftDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BaseShift
    success_url = '/'

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='Staff').exists() or user.groups.filter(name='WebAdmin').exists():
            return True
        else:
            return False