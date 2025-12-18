from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Doctor, DoctorHospital, DoctorSchedule, DoctorLeave,Specialization, DoctorSpecialization
from .serializers import (
    DoctorSerializer,
    DoctorHospitalSerializer,
    DoctorScheduleSerializer,
    DoctorLeaveSerializer,
    SpecializationSerializer,
    DoctorSpecializationSerializer,
)

@api_view(["GET"])
def doctors_view(request):

    if request.method == "GET":
        doctors = Doctor.objects.filter(is_active=True)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

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

@api_view(["GET", "POST"])
#@permission_classes([IsAuthenticated])
def specializations_view(request):

    # 🟦 GET → list all specializations
    if request.method == "GET":
        specializations = Specialization.objects.all().order_by("name")
        serializer = SpecializationSerializer(specializations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 🟩 POST → create new specialization
    elif request.method == "POST":
        serializer = SpecializationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Specialization added successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "POST"])
#@permission_classes([IsAuthenticated])
def doctor_specializations_view(request):
    """
    GET  -> list doctor-specialization mappings
    POST -> assign specialization to doctor
    """

    # 🟦 GET: list mappings with optional filters
    if request.method == "GET":
        queryset = DoctorSpecialization.objects.select_related(
            "doctor", "specialization"
        )

        doctor_id = request.query_params.get("doctor")
        specialization_id = request.query_params.get("specialization")

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)

        if specialization_id:
            queryset = queryset.filter(specialization_id=specialization_id)

        serializer = DoctorSpecializationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 🟩 POST: assign specialization to doctor
    elif request.method == "POST":
        serializer = DoctorSpecializationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Specialization assigned to doctor successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

