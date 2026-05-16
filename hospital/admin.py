from django.contrib import admin
from .models import Hospital, Service, HospitalService

admin.site.register(Hospital)
admin.site.register(Service)
admin.site.register(HospitalService)
