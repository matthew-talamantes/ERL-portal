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
    BaseShiftChildrenView,
    CalendarView,
    VolShiftSignupView,
    VolShiftUnSignupView,
    StaffShiftSignupView,
    StaffShiftUnSignupView,
)

urlpatterns = [
    path('calendar/<int:year>/<int:month>/', CalendarView.as_view(), name='shifts-calendar'),
    path('base/shifts/', BaseShiftListView.as_view(), name='base-shift-list'),
    path('base/shift/new/', BaseShiftCreateView.as_view(), name='base-shift-create'),
    path('base/shift/<slug:slug>/', BaseShiftDetailView.as_view(), name='base-shift-detail'),
    path('base/shift/<slug:slug>/update/', BaseShiftUpdateView.as_view(), name='base-shift-update'),
    path('base/shift/<slug:slug>/delete/', BaseShiftDeleteView.as_view(), name='base-shift-delete'),
    path('base/shift/<slug:slug>/shifts/', BaseShiftChildrenView.as_view(), name='base-shift-children'),
    path('base/shift/<slug:slug>/shift/new/', ShiftInstanceCreateView.as_view(), name='shift-instance-create'),
    path('base/shift/<slug:base_slug>/shift/<uuid:uid>/', ShiftInstanceDetailView.as_view(), name='shift-instance-detail'),
    path('base/shift/<slug:base_slug>/shift/<uuid:uid>/update/', ShiftInstanceUpdateView.as_view(), name='shift-instance-update'),
    path('base/shift/<slug:base_slug>/shift/<uuid:uid>/delete/', ShiftInstanceDeleteView.as_view(), name='shift-instance-delete'),
    path('base/shift/<slug:base_slug>/shift/<uuid:uid>/vol/signup/', VolShiftSignupView.as_view(), name='vol-shift-signup'),
    path('base/shift/<slug:base_slug>/shift/<uuid:uid>/vol/unsignup/', VolShiftUnSignupView.as_view(), name='vol-shift-unsignup'),
    path('', ShiftInstanceListView.as_view(), name='shift-instance-list'),
    path('base/shift/<slug:base_slug>/shift/<uuid:uid>/staff/signup/', StaffShiftSignupView.as_view(), name='staff-shift-signup'),
    path('base/shift/<slug:base_slug>/shift/<uuid:uid>/staff/unsignup/', StaffShiftUnSignupView.as_view(), name='staff-shift-unsignup'),
]