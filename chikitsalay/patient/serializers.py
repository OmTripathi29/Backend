from rest_framework import serializers
from .models import PatientProfile

class PatientProfileSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = PatientProfile
        fields = '__all__'
        read_only_fields=['user','uhid']
        