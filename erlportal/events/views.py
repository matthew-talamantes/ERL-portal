# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse, Http404
# from django.views.decorators.csrf import csrf_exempt

# from rest_framework.parsers import JSONParser
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.views import APIView

from rest_framework import generics

from .models import Event
from .serializers import EventSerializer


# Create your views here.


class EventList(generics.ListCreateAPIView):
    """
        List all events, or create a new event
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# @api_view(['GET', 'POST'])
# def event_list(request, format=None):
#     """
#         List all events or create new event
#     """
#     if request.method == 'GET':
#         events = Event.objects.all()
#         serializer = EventSerializer(events, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = EventSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        Retrieve, update or delete a snippet instance.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'slug'

# @api_view(['GET', 'PUT', 'DELETE'])
# def event_detail(request, slug, format=None):
#     """
#         Retrieve, update or delete an event.
#     """
#     try:
#         event = Event.objects.get(slug=slug)
#     except Event.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = EventSerializer(event)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = EventSerializer(event, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         event.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
