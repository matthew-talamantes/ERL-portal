from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('events/', views.event_list),
    path('events/<slug:slug>/', views.event_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)