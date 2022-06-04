from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from allauth.account.views import SignupView, ConfirmEmailView, PasswordChangeView
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import ProfileUpdateForm, ErlSignupForm
from .models import Profile, ErlUser

# Create your views here.
@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'p_form': p_form,
    }
    return render(request, 'useraccount/profile.html', context)

class ErlSignup(SignupView):
    template_name = 'account/signup.html'
    form_class = ErlSignupForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['imgFile'] = self.request.FILES
        return kwargs

class UserProfile(DetailView):
    model = Profile

class CustomPasswordChangeView(PasswordChangeView):
    success_url = '/'

class ConfirmEmailApiView(APIView, ConfirmEmailView):
    def post(self, *args, **kwargs):
        self.kwargs['key'] = self.request.data['key']
        self.object = confirmation = super().get_object()
        confirmation.confirm(self.request)
        return Response({'success': 'Email Confirmed'})

class PendingUsersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ErlUser
    template_name = 'useraccount/pending_users.html'
    context_object_name = 'users'
    paginate_by = 15
    
    def get_queryset(self):
        return ErlUser.objects.filter(groups__name='Pending')

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='Staff').exists() or user.groups.filter(name='WebAdmin').exists():
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = ErlUser.objects.filter(groups__name='Pending')
        profiles = []
        for user in users:
            try:
                profiles.append([user, Profile.objects.get(user=user)])
            except Profile.DoesNotExist:
                profiles.append([user, None])
        
        context['profiles'] = profiles
        return context

    