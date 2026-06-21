from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import PatientProfile
from .serializers import PatientProfileSerializer

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_patient_profile(request):

    if PatientProfile.objects.filter(user=request.user).exists():
        return Response(
            {"message": "Patient profile already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = PatientProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)

        return Response(
            {
                "message": "Patient profile created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_patient_profile(request):

    try:
        profile = PatientProfile.objects.get(user=request.user)

    except PatientProfile.DoesNotExist:
        return Response(
            {"message": "Profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = PatientProfileSerializer(profile)

    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_patient_by_uhid(request, uhid):

    try:
        profile = PatientProfile.objects.get(uhid=uhid)

    except PatientProfile.DoesNotExist:
        return Response(
            {"message": "Patient not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = PatientProfileSerializer(profile)

    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_patients(request):

    patients = PatientProfile.objects.all().order_by("-id")

    serializer = PatientProfileSerializer(
        patients,
        many=True
    )

    return Response(serializer.data)

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_patient_profile(request):

    try:
        profile = PatientProfile.objects.get(user=request.user)

    except PatientProfile.DoesNotExist:
        return Response(
            {"message": "Profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = PatientProfileSerializer(
        profile,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()

        return Response(
            {
                "message": "Profile updated successfully",
                "data": serializer.data
            }
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_patient_profile(request):

    try:
        profile = PatientProfile.objects.get(user=request.user)

    except PatientProfile.DoesNotExist:
        return Response(
            {"message": "Profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    profile.delete()

    return Response(
        {"message": "Profile deleted successfully"},
        status=status.HTTP_204_NO_CONTENT
    )
 