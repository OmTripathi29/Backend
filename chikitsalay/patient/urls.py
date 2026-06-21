from django.urls import path
from . import views

urlpatterns = [

    path(
        "create/",
        views.create_patient_profile,
        name="create-patient-profile"
    ),

    path(
        "me/",
        views.get_patient_profile,
        name="my-patient-profile"
    ),

    path(
        "all/",
        views.get_all_patients,
        name="all-patients"
    ),

    path(
        "update/",
        views.update_patient_profile,
        name="update-patient-profile"
    ),

    path(
        "delete/",
        views.delete_patient_profile,
        name="delete-patient-profile"
    ),

    path(
        "<str:uhid>/",
        views.get_patient_by_uhid,
        name="patient-by-uhid"
    ),
]