from rest_framework import serializers
from .models import HospitalService,Service,Hospital


class HospitalServiceSearchSerializer(serializers.ModelSerializer):
   
    hospital_name = serializers.CharField(source="hospital.name", read_only=True)
    hospital_address = serializers.CharField(source="hospital.address", read_only=True)
    hospital_phone = serializers.CharField(source="hospital.phone", read_only=True)
    service_name = serializers.CharField(source="service.name", read_only=True)
    latitude = serializers.DecimalField(
        source="hospital.latitude",
        max_digits=9,
        decimal_places=6,
        read_only=True,
    )
    longitude = serializers.DecimalField(
        source="hospital.longitude",
        max_digits=9,
        decimal_places=6,
        read_only=True,
    )
    distance_km = serializers.FloatField(read_only=True)

    class Meta:
        model = HospitalService
        fields = [
            "id",
            "hospital_name",
            "hospital_address",
            "hospital_phone",
            "service_name",
            "price",
            "latitude",
            "longitude",
            "distance_km",
        ]
class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name"]


class HospitalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = [
            "id",
            "name",
            "address",
            "phone",
            "latitude",
            "longitude",
            "rating"
        ]


class HospitalServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalService
        fields = ["id", "hospital", "service", "price"]