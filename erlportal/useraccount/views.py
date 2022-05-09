from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from allauth.account.views import SignupView, ConfirmEmailView
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import ProfileUpdateForm, ErlSignupForm
from .models import Profile

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

class ConfirmEmailApiView(APIView, ConfirmEmailView):
    def post(self, *args, **kwargs):
        self.kwargs['key'] = self.request.data['key']
        self.object = confirmation = super().get_object()
        confirmation.confirm(self.request)
        return Response({'success': 'Email Confirmed'})

    