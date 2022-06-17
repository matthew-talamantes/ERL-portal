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
class BaseShiftListView(LoginRequiredMixin, ListView):
    model = BaseShift
    context_object_name = 'shifts'
    ordering = ['name']
    paginate_by = 25

class BaseShiftDetailView(LoginRequiredMixin, DetailView):
    model = BaseShift

class BaseShiftCreateView(LoginRequiredMixin, CreateView):
    model = BaseShift
    fields = ['name', 'description', 'startTime', 'endTime', 'repeat', 'endRepeat', 'minSlots', 'staffSlots', 'volSlots', 'defaultStaff', 'defaultVols']

    def get_form(self):
        form = super().get_form()
        form.fields['startTime'].widget = TextInput(attrs={'type': 'datetime-local'})
        form.fields['endTime'].widget = TextInput(attrs={'type': 'datetime-local'})
        return form

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        return super().form_valid(form)

class BaseShiftUpdateView(LoginRequiredMixin, UpdateView):
    model = BaseShift
    fields = ['name', 'description', 'startTime', 'endTime', 'repeat', 'endRepeat', 'minSlots', 'staffSlots', 'volSlots', 'defaultStaff', 'defaultVols']

    def get_form(self):
        form = super().get_form()
        form.fields['startTime'].widget = TextInput(attrs={'type': 'datetime-local'})
        form.fields['endTime'].widget = TextInput(attrs={'type': 'datetime-local'})
        return form

class BaseShiftDeleteView(LoginRequiredMixin, DeleteView):
    model = BaseShift
    success_url = '/'