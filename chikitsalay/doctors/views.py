from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Doctor, DoctorHospital, DoctorSchedule, DoctorLeave
from .serializers import (
    DoctorSerializer,
    DoctorHospitalSerializer,
    DoctorScheduleSerializer,
    DoctorLeaveSerializer,
)

@api_view(["GET", "POST"])
#@permission_classes([IsAuthenticated])
def doctors_view(request):

    if request.method == "GET":
        doctors = Doctor.objects.filter(is_active=True)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(["GET", "POST"])
#@permission_classes([IsAuthenticated])
def doctors_view(request):

    if request.method == "GET":
        doctors = Doctor.objects.filter(is_active=True)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
@api_view(["GET", "PATCH", "DELETE"])
#@permission_classes([IsAuthenticated])
def doctor_detail_view(request, doctor_id):

    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "GET":
        return Response(DoctorSerializer(doctor).data)

    if request.method == "PATCH":
        serializer = DoctorSerializer(
            doctor, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        doctor.is_active = False
        doctor.save()
        return Response({"message": "Doctor deactivated"}, status=204)
@api_view(["POST"])
#@permission_classes([IsAuthenticated])
def assign_doctor_to_hospital(request):
    serializer = DoctorHospitalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
@api_view(["POST"])
#@permission_classes([IsAuthenticated])
def add_doctor_schedule(request):
    serializer = DoctorScheduleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
@api_view(["DELETE"])
#@permission_classes([IsAuthenticated])
def delete_doctor_schedule(request, schedule_id):
    schedule = get_object_or_404(DoctorSchedule, id=schedule_id)
    schedule.delete()
    return Response({"message": "Schedule removed"}, status=204)
@api_view(["POST"])
#@permission_classes([IsAuthenticated])
def add_doctor_leave(request):
    serializer = DoctorLeaveSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
@api_view(["DELETE"])
#@permission_classes([IsAuthenticated])
def delete_doctor_leave(request, leave_id):
    leave = get_object_or_404(DoctorLeave, id=leave_id)
    leave.delete()
    return Response({"message": "Leave removed"}, status=204)

