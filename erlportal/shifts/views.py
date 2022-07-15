from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.forms import HiddenInput, TextInput

from .models import BaseShift, ShiftInstance

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

class ShiftInstanceListView(LoginRequiredMixin, ListView):
    model = ShiftInstance
    context_object_name = 'shifts'
    ordering = ['date', 'startTime']
    paginate_by = 25

class ShiftInstanceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ShiftInstance
    fields = ['name', 'baseShift','description', 'date', 'startTime', 'endTime', 'staffSlots', 'volSlots', 'minSlots', 'staff', 'vols']

    def get_initial(self):
        baseShift = get_object_or_404(BaseShift, slug=self.kwargs.get('slug'))
        defaultStaff = baseShift.defaultStaff.all()
        defaultVols = baseShift.defaultVols.all()
        initialDict = {'baseShift': baseShift, 'staff': defaultStaff, 'vols': defaultVols, 'name': baseShift.name, 'description': baseShift.description, 'startTime': baseShift.startTime, 'endTime': baseShift.endTime, 'staffSlots': baseShift.staffSlots, 'volSlots': baseShift.volSlots, 'minSlots': baseShift.minSlots, 'date': baseShift.date}
        return initialDict

    def get_form(self):
        form = super().get_form()
        form.fields['baseShift'].widget = HiddenInput()
        form.fields['date'].widget = TextInput(attrs={'type': 'date'})
        form.fields['startTime'].widget = TextInput(attrs={'type': 'time'})
        form.fields['endTime'].widget = TextInput(attrs={'type': 'time'})
        return form

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='Staff').exists() or user.groups.filter(name='WebAdmin').exists():
            return True
        else:
            return False

class ShiftInstanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ShiftInstance
    fields = ['name', 'description', 'date', 'startTime', 'endTime', 'staffSlots', 'volSlots', 'minSlots', 'staff', 'vols']
    
    def get_object(self, queryset=None):
        uid = self.kwargs['uid']
        shift = get_object_or_404(ShiftInstance, uid=uid)
        return shift

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = TextInput(attrs={'type': 'date'})
        form.fields['startTime'].widget = TextInput(attrs={'type': 'time'})
        form.fields['endTime'].widget = TextInput(attrs={'type': 'time'})
        return form

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='Staff').exists() or user.groups.filter(name='WebAdmin').exists():
            return True
        else:
            return False

class ShiftInstanceDetailView(LoginRequiredMixin, DetailView):
    model = ShiftInstance

    def get_object(self, queryset=None):
        uid = self.kwargs['uid']
        shift = get_object_or_404(ShiftInstance, uid=uid)
        return shift

class ShiftInstanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ShiftInstance
    success_url = '/'

    def get_object(self, queryset=None):
        uid = self.kwargs['uid']
        shift = get_object_or_404(ShiftInstance, uid=uid)
        return shift

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='Staff').exists() or user.groups.filter(name='WebAdmin').exists():
            return True
        else:
            return False

class BaseShiftChildrenView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ShiftInstance
    paginate_by = 25
    context_object_name = 'shifts'
    template_name = 'shifts/children_shifts.html'

    def get_queryset(self):
        baseShift = get_object_or_404(BaseShift, slug=self.kwargs.get('slug'))
        return ShiftInstance.objects.filter(baseShift=baseShift).order_by('-startTime')


