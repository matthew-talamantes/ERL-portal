from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

from allauth.account.views import SignupView

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

# class ErlSignup(SignupView):
#     template_name = 'account/signup.html'
#     profileForm = ProfileUpdateForm()

#     def form_valid(self, form):
#         context = self.get_context_data()
#         signupForm = context['form']
#         profileForm = context['profileForm']
#         if signupForm.is_valid():
#             user = signupForm.save(self.request)
#             profileForm.user = user
#         if signupForm.is_valid() and profileForm.is_valid():
#             signupForm.save()
#             profileForm.save()
#             super().form_valid(form)



#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['profileForm'] = self.profileForm
#         return context

class UserProfile(DetailView):
    model = Profile