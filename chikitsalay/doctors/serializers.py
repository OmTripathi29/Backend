from rest_framework import serializers
from .models import Doctor, DoctorHospital, DoctorSchedule, DoctorLeave, Specialization, DoctorSpecialization


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"
class DoctorHospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorHospital
        fields = "__all__"
class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = "__all__"
class DoctorLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorLeave
        fields = "__all__"
class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ["id", "name"]
        
class DoctorSpecializationSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source="doctor.name", read_only=True)
    specialization_name = serializers.CharField(source="specialization.name", read_only=True)

    class Meta:
        model = DoctorSpecialization
        fields = [
            "id",
            "doctor",
            "doctor_name",
            "specialization",
            "specialization_name",
        ]

