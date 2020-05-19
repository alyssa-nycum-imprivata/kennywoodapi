"""Itineraries for Kennywood Amusement Park"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Itinerary


class ItinerarySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for itineraries

    Arguments:
        serializers
    """
    class Meta:
        model = Itinerary
        url = serializers.HyperlinkedIdentityField(
            view_name='itinerary',
            lookup_field='id'
        )
        fields = ('id', 'url', 'starttime', 'attraction_id', 'customer_id')

class Itineraries(ViewSet):
    """Itineraries for Kennywood Amusement Park"""

    def list(self, request):
        """Handle GET requests to itineraries resource

        Returns:
            Response -- JSON serialized list of itineraries
        """
        itineraries = Itinerary.objects.all()
        serializer = ItinerarySerializer(
            itineraries, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single itinerary

        Returns:
            Response -- JSON serialized itinerary instance
        """
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            serializer = ItinerarySerializer(itinerary, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Itinerary instance
        """
        newitinerary = Itinerary()
        newitinerary.starttime = request.data['starttime']
        newitinerary.attraction_id = request.data['attraction_id']
        newitinerary.customer_id = request.data['customer_id']
        newitinerary.save()

        serializer = ItinerarySerializer(newitinerary, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for an itinerary

        Returns:
            Response -- Empty body with 204 status code
        """
        itinerary = Itinerary.objects.get(pk=pk)
        itinerary.starttime = request.data['starttime']
        itinerary.attraction_id = request.data['attraction_id']
        itinerary.customer_id = request.data['customer_id']
        itinerary.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single itinerary

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            itinerary.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Itinerary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)