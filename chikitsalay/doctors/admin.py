from django.contrib import admin
from .models import Doctor, Specialization, DoctorSpecialization, DoctorHospital, DoctorSchedule

admin.site.register(Doctor)
admin.site.register(Specialization) 
admin.site.register(DoctorSpecialization)
admin.site.register(DoctorHospital)
admin.site.register(DoctorSchedule)

