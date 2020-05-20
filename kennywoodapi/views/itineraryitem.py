"""Itineraries for Kennywood Amusement Park"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Itinerary, Customer, Attraction


class ItineraryItemSerializer(serializers.HyperlinkedModelSerializer):
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
        fields = ('id', 'url', 'starttime', 'attraction')
        depth = 1

class ItineraryItems(ViewSet):
    """Itineraries for Kennywood Amusement Park"""

    def list(self, request):
        """Handle GET requests to itineraries resource

        Returns:
            Response -- JSON serialized list of itineraries
        """
        customer = Customer.objects.get(user=request.auth.user)

        itinerary_items = Itinerary.objects.filter(customer=customer)

        serializer = ItineraryItemSerializer(
            itinerary_items, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single itinerary

        Returns:
            Response -- JSON serialized itinerary instance
        """
        try:
            itinerary_item = Itinerary.objects.get(pk=pk)
            serializer = ItineraryItemSerializer(itinerary_item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Itinerary instance
        """
        attraction = Attraction.objects.get(pk=request.data["ride_id"])
        customer = Customer.objects.get(user=request.auth.user)

        new_itinerary_item = Itinerary()
        new_itinerary_item.starttime = request.data['starttime']
        new_itinerary_item.customer = customer
        new_itinerary_item.attraction = attraction
        
        new_itinerary_item.save()

        serializer = ItineraryItemSerializer(new_itinerary_item, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for an itinerary

        Returns:
            Response -- Empty body with 204 status code
        """
        itinerary_item = Itinerary.objects.get(pk=pk)
        itinerary_item.starttime = request.data['starttime']

        attraction = Attraction.objects.get(pk=request.data["attraction_id"])
        itinerary_item.attraction = attraction
        
        itinerary_item.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single itinerary

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            itinerary_item = Itinerary.objects.get(pk=pk)
            itinerary_item.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Itinerary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)