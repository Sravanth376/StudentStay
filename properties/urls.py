from django.urls import path
from .views import (
    PropertyListCreateAPIView,
    PropertyDetailAPIView,
    ToggleFavoriteAPIView,
    FavoritePropertyListAPIView,
    ReviewListCreateAPIView,
    ReviewDetailAPIView,
    MyPropertiesAPIView,
    BookingCreateAPIView,
    MyBookingsAPIView,
    OwnerBookingsAPIView,
    ApproveBookingAPIView,
    RejectBookingAPIView,
    OwnerDashboardAPIView,
)

urlpatterns = [
    path("", PropertyListCreateAPIView.as_view(), name="property-list"),

    path(
        "favorites/",
        FavoritePropertyListAPIView.as_view(),
        name="favorite-properties",
    ),

    path(
    "dashboard/my-properties/",
    MyPropertiesAPIView.as_view(),
    name="my-properties",
    ),

    path(
    "bookings/",
    MyBookingsAPIView.as_view(),
    name="my-bookings",
    ),

    path(
    "dashboard/bookings/",
    OwnerBookingsAPIView.as_view(),
    name="owner-bookings",
    ),

    path(
    "dashboard/stats/",
    OwnerDashboardAPIView.as_view(),
    name="owner-dashboard",
    ),

    path(
    "bookings/<int:pk>/approve/",
    ApproveBookingAPIView.as_view(),
    name="approve-booking",
    ),

    path(
    "bookings/<int:pk>/reject/",
    RejectBookingAPIView.as_view(),
    name="reject-booking",
    ),

    path(
    "<int:pk>/book/",
    BookingCreateAPIView.as_view(),
    name="book-property",
    ),

    path("<int:pk>/", PropertyDetailAPIView.as_view(), name="property-detail"),

    path(
        "<int:pk>/favorite/",
        ToggleFavoriteAPIView.as_view(),
        name="toggle-favorite",
    ),
    path(
    "<int:pk>/reviews/",
    ReviewListCreateAPIView.as_view(),
    name="property-reviews",
    ),

    path(
        "reviews/<int:pk>/",
        ReviewDetailAPIView.as_view(),
        name="review-delete",
    ),
]