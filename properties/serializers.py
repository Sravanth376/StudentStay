from rest_framework import serializers
from .models import Property, Review, Booking
from .utils import calculate_distance

SRKR_LAT = 16.544900
SRKR_LON = 81.521200


class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    owner_name = serializers.SerializerMethodField()

    distance = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            "id",
            "owner",
            "owner_name",
            "title",
            "description",
            "city",
            "address",
            "property_type",
            "gender",
            "available_rooms",
            "is_available",
            "rent",
            "image",
            "latitude",
            "longitude",
            "distance",
            "average_rating",
            "total_reviews",
            "created_at",
        ]
        read_only_fields = ["owner"]

    def get_owner_name(self, obj):
        full_name = f"{obj.owner.first_name} {obj.owner.last_name}".strip()
        return full_name if full_name else obj.owner.email.split("@")[0]

    def get_distance(self, obj):
        if obj.latitude is None or obj.longitude is None:
            return None

        return calculate_distance(
            SRKR_LAT,
            SRKR_LON,
            float(obj.latitude),
            float(obj.longitude),
        )

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()

        if not reviews.exists():
            return 0

        total = sum(review.rating for review in reviews)
        return round(total / reviews.count(), 1)

    def get_total_reviews(self, obj):
        return obj.reviews.count()
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = ["user", "created_at"]   

class BookingSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    property_title = serializers.CharField(
        source="property.title",
        read_only=True,
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "student",
            "property",
            "property_title",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "student",
            "property",
            "status",
            "created_at",
        ]        