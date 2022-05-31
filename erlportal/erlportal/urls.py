"""erlportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from dj_rest_auth.registration.views import VerifyEmailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from useraccount.views import ErlSignup, ConfirmEmailApiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', ErlSignup.as_view(), name='signup'),
    path('accounts/', include('useraccount.urls')),
    path('', include('pages.urls')),
    path('api-auth/', include('dj_rest_auth.urls')),
    path('api-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api-auth/registration/account-confirm-email/', ConfirmEmailApiView.as_view(), name='confrim-email'),
    path('api-auth/registration/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('api-auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # For rest tutorial rewrite for actual release
    path('events/', include('events.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
