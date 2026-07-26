from rest_framework import serializers
from .models import Property
from .utils import calculate_distance


SRKR_LAT = 16.544900
SRKR_LON = 81.521200


class PropertySerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = "__all__"
        # Because we're using "__all__", the model fields are included automatically.
        # SerializerMethodField is added automatically as well.

    def get_distance(self, obj):
        if obj.latitude is None or obj.longitude is None:
            return None

        return calculate_distance(
            SRKR_LAT,
            SRKR_LON,
            float(obj.latitude),
            float(obj.longitude),
        )