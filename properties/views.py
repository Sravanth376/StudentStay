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
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.exceptions import ValidationError
from .models import Booking
from .serializers import BookingSerializer
class PropertyListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer

    SRKR_LAT = 16.544900
    SRKR_LON = 81.521200

    def get_queryset(self):
        queryset = Property.objects.all()

        city = self.request.query_params.get("city")
        property_type = self.request.query_params.get("property_type")
        gender = self.request.query_params.get("gender")
        min_rent = self.request.query_params.get("min_rent")
        max_rent = self.request.query_params.get("max_rent")

        if city:
            queryset = queryset.filter(city__iexact=city)

        if property_type:
            queryset = queryset.filter(property_type=property_type)

        if gender:
            queryset = queryset.filter(gender=gender)

        if min_rent:
            queryset = queryset.filter(rent__gte=min_rent)

        if max_rent:
            queryset = queryset.filter(rent__lte=max_rent)

        ordering = self.request.query_params.get("ordering")

        allowed_ordering = [
            "rent",
            "-rent",
            "created_at",
            "-created_at",
        ]

        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)    

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

class FavoritePropertyListAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.favorite_properties.all()    

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(
            property_id=self.kwargs["pk"]
        ).order_by("-created_at")

    def perform_create(self, serializer):
        property_obj = Property.objects.get(pk=self.kwargs["pk"])

        if Review.objects.filter(
            property=property_obj,
            user=self.request.user
        ).exists():
            raise ValidationError(
                {"error": "You have already reviewed this property."}
            )

        serializer.save(
            user=self.request.user,
            property=property_obj
        )


class ReviewDetailAPIView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)    

class MyPropertiesAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user) 

class BookingCreateAPIView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        property_obj = Property.objects.get(pk=self.kwargs["pk"])

        if not property_obj.is_available or property_obj.available_rooms <= 0:
            raise ValidationError(
                {"error": "No rooms are available for this property."}
            )

        if Booking.objects.filter(
            property=property_obj,
            student=self.request.user,
        ).exists():
            raise ValidationError(
                {"error": "You have already booked this property."}
            )

        serializer.save(
            student=self.request.user,
            property=property_obj,
        )

class MyBookingsAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            student=self.request.user
        ).order_by("-created_at") 

class OwnerBookingsAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            property__owner=self.request.user
        ).order_by("-created_at")  

class OwnerDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        properties = Property.objects.filter(owner=request.user)

        bookings = Booking.objects.filter(
            property__owner=request.user
        )

        data = {
            "total_properties": properties.count(),
            "total_bookings": bookings.count(),
            "pending_bookings": bookings.filter(
                status="PENDING"
            ).count(),
            "approved_bookings": bookings.filter(
                status="APPROVED"
            ).count(),
            "rejected_bookings": bookings.filter(
                status="REJECTED"
            ).count(),
        }

        return Response(data)
class ApproveBookingAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)

        if booking.property.owner != request.user:
            return Response(
                {"error": "You are not allowed to approve this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if booking.status != "PENDING":
            return Response(
                {"error": "Only pending bookings can be approved."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        booking.approve()

        return Response(
            {"message": "Booking approved successfully."},
            status=status.HTTP_200_OK,
        ) 

class RejectBookingAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)

        if booking.property.owner != request.user:
            return Response(
                {"error": "You are not allowed to reject this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if booking.status != "PENDING":
            return Response(
                {"error": "Only pending bookings can be rejected."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.reject()

        return Response(
            {"message": "Booking rejected successfully."},
            status=status.HTTP_200_OK,
        )                     