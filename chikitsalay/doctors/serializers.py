from rest_framework import serializers
from .models import Doctor, DoctorHospital, DoctorSchedule, DoctorLeave


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
