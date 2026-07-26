from django.urls import path
from .views import (
    PropertyListCreateAPIView,
    PropertyDetailAPIView,
    ToggleFavoriteAPIView,
)
urlpatterns = [
    path("properties/", PropertyListCreateAPIView.as_view()),
    path("properties/<int:pk>/", PropertyDetailAPIView.as_view()),
    path(
        "properties/<int:pk>/favorite/",
        ToggleFavoriteAPIView.as_view(),
        name="toggle-favorite",
    ),
]