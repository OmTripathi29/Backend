from django.db import models
from django.conf import settings
import uuid

def generate_uhid():
    return f"UHID-{(uuid.uuid4().hex[:12].upper())}"
class PatientProfile(models.Model):
    GENDER_CHOICES = [("MALE","Male"),("FEMALE","Female"),("OTHER","Other")]
    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='patient_profile')
    uhid = models.CharField(max_length=20, unique=True,default=generate_uhid,editable=False)
    name = models.CharField(max_length=300,null=False,blank=False,default="Patient")
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=20, null=True, blank=True)

        
    def __str__(self):
        return f"{self.name} - {self.uhid}"
    
    