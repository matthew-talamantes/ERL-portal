from django.urls import path, include

from .views import profile, UserProfile, GetCSRFToken

urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/', profile, name='profile'),
    path('profile/<slug:slug>/', UserProfile.as_view(), name='user-profile'),
    path('csrf_cookie/', GetCSRFToken.as_view(), name='get-csrf-token'),
]
