from rest_framework import serializers

from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['uid', 'title', 'eventType', 'year', 'month', 'day', 'startTime', 'endTime', 'description', 'slug', 'dateCreated']