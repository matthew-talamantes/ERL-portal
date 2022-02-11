from rest_framework import serializers

from .models import Event

class EventSerializer(serializers.ModelSerializer):

    def validate(self, data):
        
        if data['endTime'] <= data['startTime']:
            raise serializers.ValidationError('End Time must be after Start Time.')
        return data

    class Meta:
        model = Event
        fields = ['uid', 'title', 'eventType', 'startTime', 'endTime', 'description', 'slug', 'dateCreated']