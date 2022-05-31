from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('event/new/', views.EventCreateView.as_view(), name='event-create'),
    path('event/<slug:slug>/', views.EventDetailView.as_view(), name='event-detail'),
    path('event/<slug:slug>/update/', views.EventUpdateView.as_view(), name='event-update'),
    path('event/<slug:slug>/delete/', views.EventDeleteView.as_view(), name='event-delete'),
    path('api/', include('rest_framework.urls')),
    path('api/events', views.EventList.as_view(), name='event-list-endpoint'),
    path('api/event/<slug:slug>/', views.EventDetail.as_view(), name='event-detail-endpoint'),
    path('calendar/<int:year>/<int:month>/', views.CalendarView.as_view(), name='events-calendar'),
]

urlpatterns = format_suffix_patterns(urlpatterns)