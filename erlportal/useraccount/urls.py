from django.urls import path, include

from .views import profile, UserProfile, CustomPasswordChangeView, PendingUsersListView

urlpatterns = [
    path('password/change/', CustomPasswordChangeView.as_view(), name='account_password_change'),
    path('profile/', profile, name='profile'),
    path('profile/<slug:slug>/', UserProfile.as_view(), name='user-profile'),
    path('pending-users/', PendingUsersListView.as_view(), name='pending-users'),
    path('', include('allauth.urls')),
]
