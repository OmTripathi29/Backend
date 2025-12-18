from django.urls import path
from .views import (
    doctors_view,
    doctor_detail_view,
    assign_doctor_to_hospital,
    add_doctor_schedule,
    delete_doctor_schedule,
    add_doctor_leave,
    delete_doctor_leave,
)

urlpatterns = [
    # Doctor CRUD
    path("doctors/", doctors_view),
    path("doctors/<int:doctor_id>/", doctor_detail_view),

    # Doctor ↔ Hospital
    path("assign-hospital/", assign_doctor_to_hospital),

    # Schedule
    path("schedule/add/", add_doctor_schedule),
    path("schedule/<int:schedule_id>/delete/", delete_doctor_schedule),

    # Leave
    path("leave/add/", add_doctor_leave),
    path("leave/<int:leave_id>/delete/", delete_doctor_leave),
]
