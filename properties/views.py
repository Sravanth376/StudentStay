from rest_framework import generics
from .models import Property
from .serializers import PropertySerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .utils import calculate_distance
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

class PropertyListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer

    SRKR_LAT = 16.544900
    SRKR_LON = 81.521200

    def get_queryset(self):
        queryset = Property.objects.all()
        search = self.request.query_params.get("search")
        city = self.request.query_params.get("city")
        min_rent = self.request.query_params.get("min_rent")
        max_rent = self.request.query_params.get("max_rent")
        max_distance = self.request.query_params.get("max_distance")

        if city:
            queryset = queryset.filter(city__iexact=city)

        if min_rent:
            queryset = queryset.filter(rent__gte=min_rent)

        if max_rent:
            queryset = queryset.filter(rent__lte=max_rent)
        if search:
                queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(city__icontains=search) |
                Q(description__icontains=search)
                ) 
        if max_distance:
            filtered = []

          

            for prop in queryset:
                if prop.latitude and prop.longitude:
                    distance = calculate_distance(
                        self.SRKR_LAT,
                        self.SRKR_LON,
                        float(prop.latitude),
                        float(prop.longitude),
                    )

                    if distance <= float(max_distance):
                        filtered.append(prop)

            return filtered

        return queryset


class PropertyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

class ToggleFavoriteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        prop = get_object_or_404(Property, pk=pk)

        prop.favorites.add(request.user)

        return Response(
            {"message": "Property added to favorites."},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        prop = get_object_or_404(Property, pk=pk)

        prop.favorites.remove(request.user)

        return Response(
            {"message": "Property removed from favorites."},
            status=status.HTTP_200_OK,
        )