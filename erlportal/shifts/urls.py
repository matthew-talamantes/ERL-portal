from django.urls import path, include

from .views import (
    BaseShiftCreateView,
    BaseShiftUpdateView,
    BaseShiftDetailView,
    BaseShiftDeleteView,
    BaseShiftListView,
    ShiftInstanceCreateView,
    ShiftInstanceListView,
    ShiftInstanceDetailView,
    ShiftInstanceUpdateView,
    ShiftInstanceDeleteView,
)

urlpatterns = [
    path('base/shifts/', BaseShiftListView.as_view(), name='base-shift-list'),
    path('base/shift/new/', BaseShiftCreateView.as_view(), name='base-shift-create'),
    path('base/shift/<slug:slug>/', BaseShiftDetailView.as_view(), name='base-shift-detail'),
    path('base/shift/<slug:slug>/update/', BaseShiftUpdateView.as_view(), name='base-shift-update'),
    path('base/shift/<slug:slug>/delete/', BaseShiftDeleteView.as_view(), name='base-shift-delete'),
    path('base/shift/<slug:slug>/shift/new/', ShiftInstanceCreateView.as_view(), name='shift-instance-create'),
    path('base/shift/<slug:base_slug>/shift/<uuid:uid>/', ShiftInstanceDetailView.as_view(), name='shift-instance-detail'),
    path('base/shift/<slug:base_slug>/shift/<uuid:uid>/update/', ShiftInstanceUpdateView.as_view(), name='shift-instance-update'),
    path('base/shift/<slug:base_slug>/shift/<uuid:uid>/delete/', ShiftInstanceDeleteView.as_view(), name='shift-instance-delete'),
    path('', ShiftInstanceListView.as_view(), name='shift-instance-list'),
]