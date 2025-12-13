from django.urls import path
from .views import hospital_search, add_service, add_hospital, add_hospital_service,get_all_hospitals, update_hospital,delete_hospital

urlpatterns = [
    path("search/", hospital_search, name="hospital-search"),
    path("get_all_clinics/", get_all_hospitals, name="all-hospitals"),
    path("services/", add_service, name="add-service"),
    path("services/clinic/", add_hospital, name="add-hospital"),
    path("services/hospital-service/", add_hospital_service, name="add-hospital-service"),
    path("clinic/<int:hospital_id>/", update_hospital, name="update-hospital"),
    path("clinic/delete/<int:hospital_id>/", delete_hospital, name="delete-hospital"),
    
]