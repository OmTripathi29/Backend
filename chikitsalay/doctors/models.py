from django.db import models
from hospital.models import Hospital


class Doctor(models.Model):
    name = models.CharField(max_length=255)

    # Image upload (stored locally or cloud later)
    profile_image = models.ImageField(
        upload_to="doctors/profile_images/",
        blank=True,
        null=True
    )

    experience_years = models.PositiveIntegerField(null=True, blank=True)
    about = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class DoctorSpecialization(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("doctor", "specialization")

class DoctorHospital(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="doctor_hospitals"
    )
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="hospital_doctors"
    )

    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("doctor", "hospital")

    def __str__(self):
        return f"{self.doctor.name} @ {self.hospital.name}"


class DoctorSchedule(models.Model):
    WEEK_DAYS = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    doctor_hospital = models.ForeignKey(
        DoctorHospital,
        on_delete=models.CASCADE,
        related_name="schedules"
    )

    day_of_week = models.IntegerField(choices=WEEK_DAYS)

    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = (
            "doctor_hospital",
            "day_of_week",
            "start_time",
            "end_time",
        )

class DoctorLeave(models.Model):
    doctor_hospital = models.ForeignKey(
        DoctorHospital,
        on_delete=models.CASCADE,
        related_name="leaves"
    )

    date = models.DateField()
    reason = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("doctor_hospital", "date")