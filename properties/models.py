from django.db import models
from django.conf import settings
from django.conf import settings
class Property(models.Model):

    latitude = models.DecimalField(
    max_digits=9,
    decimal_places=6,
    null=True,
    blank=True
    )

    longitude = models.DecimalField(
    max_digits=9,
    decimal_places=6,
    null=True,
    blank=True
    )

    PROPERTY_TYPES = [
        ("HOSTEL", "Hostel"),
        ("PG", "PG"),
        ("APARTMENT", "Apartment"),
    ]

    GENDER_CHOICES = [
        ("BOYS", "Boys"),
        ("GIRLS", "Girls"),
        ("UNISEX", "Unisex"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES,
        default="HOSTEL"
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default="UNISEX"
    )

    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="favorite_properties",
        blank=True
    )

    available_rooms = models.PositiveIntegerField(default=1)

    is_available = models.BooleanField(default=True)

    rent = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(
        upload_to="properties/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title