from django.urls import path, include

from .views import (
    BaseShiftCreateView,
    BaseShiftUpdateView,
    BaseShiftDetailView,
    BaseShiftDeleteView,
    BaseShiftListView,
)

urlpatterns = [
    path('base/shifts/', BaseShiftListView.as_view(), name='base-shift-list'),
    path('base/shift/new/', BaseShiftCreateView.as_view(), name='base-shift-create'),
    path('base/shift/<slug:slug>/', BaseShiftDetailView.as_view(), name='base-shift-detail'),
    path('base/shift/<slug:slug>/update/', BaseShiftUpdateView.as_view(), name='base-shift-update'),
    path('base/shift/<slug:slug>/delete/', BaseShiftDeleteView.as_view(), name='base-shift-delete'),

]