from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

from .forms import ProfileUpdateForm
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
    return render(request, 'useraccounts/profile.html', context)

class UserProfile(DetailView):
    model = Profile