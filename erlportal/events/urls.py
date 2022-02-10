from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('events/', views.EventList.as_view(), name='eventListEndpoint'),
    path('events/<slug:slug>/', views.EventDetail.as_view(), name='eventDetailEndpoint'),
]

urlpatterns = format_suffix_patterns(urlpatterns)