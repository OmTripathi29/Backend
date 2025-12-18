from math import radians, cos, sin, acos
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Service, HospitalService, Hospital
from .serializers import HospitalServiceSearchSerializer, ServiceCreateSerializer, HospitalCreateSerializer, HospitalServiceCreateSerializer


@api_view(['GET'])
##@permission_classes([IsAuthenticated])  
def hospital_search(request):
    service_query = request.query_params.get("service")
    lat = request.query_params.get("lat")
    lon = request.query_params.get("lon")
    sort = request.query_params.get("sort", "distance").lower()
    max_distance_km = request.query_params.get("max_distance_km")

    if not service_query:
        return Response({"detail": "Parameter 'service' is required."}, status=400)

    if lat is None or lon is None:
        return Response({"detail": "Parameters 'lat' and 'lon' are required."}, status=400)

    try:
        user_lat = float(lat)
        user_lon = float(lon)
    except ValueError:
        return Response({"detail": "Invalid lat/lon values."}, status=400)


    services = Service.objects.filter(name__icontains=service_query)
    if not services.exists():
        return Response([], status=200)
    
    service = services.first()


    hospital_services = HospitalService.objects.filter(service=service).select_related('hospital')

    results = []
    for hs in hospital_services:
        h = hs.hospital
        distance = haversine(user_lat, user_lon, float(h.latitude), float(h.longitude))
        hs.distance_km = round(distance, 3)

        if max_distance_km:
            try:
                max_dist = float(max_distance_km)
                if hs.distance_km > max_dist:
                    continue
            except ValueError:
                pass  # ignore incorrect filter

        results.append(hs)

    # Sorting logic
    if sort == "price":
        results.sort(key=lambda x: (x.price, x.distance_km))
    else:
        results.sort(key=lambda x: (x.distance_km, x.price))

    # Paginate response
    paginator = LimitOffsetPagination()
    paginated = paginator.paginate_queryset(results, request)

    serializer = HospitalServiceSearchSerializer(paginated, many=True)
    return paginator.get_paginated_response(serializer.data)


def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance in km using Haversine formula"""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return 6371 * acos(
        cos(lat1) * cos(lat2) * cos(lon2 - lon1) +
        sin(lat1) * sin(lat2)
    )

@api_view(['POST','GET'])
##@permission_classes([IsAuthenticated])
def add_service(request):
    
    if request.method == "GET":
        services = Service.objects.all().order_by("name")
        serializer = ServiceCreateSerializer(services, many=True)
        return Response(serializer.data, status=200)
    serializer = ServiceCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Service added successfully", "data": serializer.data}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
##@permission_classes([IsAuthenticated])
def add_hospital(request):
    serializer = HospitalCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Hospital added successfully", "data": serializer.data}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
##@permission_classes([IsAuthenticated])
def add_hospital_service(request):
    serializer = HospitalServiceCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Hospital service added successfully", "data": serializer.data}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_all_hospitals(request):
    hospitals = Hospital.objects.all().order_by("name")
    serializer = HospitalCreateSerializer(hospitals, many=True)
    return Response(serializer.data, status=200)

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_hospital(request, hospital_id):


    hospital = get_object_or_404(Hospital, id=hospital_id)

    serializer = HospitalCreateSerializer(
        hospital,
        data=request.data,
        partial=(request.method == "PATCH")
    )

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Hospital updated successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_hospital(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    hospital.delete()
    return Response(
        {"message": "Hospital deleted successfully"},
        status=status.HTTP_204_NO_CONTENT
    )
