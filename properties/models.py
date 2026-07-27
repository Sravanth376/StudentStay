from django.db import models
from django.conf import settings
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


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

class Review(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["property", "user"],
                name="unique_review_per_user"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.property} ({self.rating})"  

class Booking(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING",
    )


    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student} → {self.property} ({self.status})"  
    
    def approve(self):
        if self.status != "PENDING":
            return

        property_obj = self.property

        if property_obj.available_rooms > 0:
            property_obj.available_rooms -= 1

            if property_obj.available_rooms == 0:
                property_obj.is_available = False

            property_obj.save()

        self.status = "APPROVED"
        self.save()

    def reject(self):
        self.status = "REJECTED"
        self.save()    