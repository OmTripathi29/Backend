from math import radians, cos, sin, acos
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status

from .models import Service, HospitalService
from .serializers import HospitalServiceSearchSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])  
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
