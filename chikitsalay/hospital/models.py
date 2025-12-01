from django.db import models

# Create your models here.
class Hospital(models.Model):
    
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=120, unique=True, db_index=True)
    def __str__(self) -> str:
        return self.name

class HospitalService(models.Model):
  
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="hospital_services",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="service_hospitals",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("hospital", "service")
        indexes = [
            models.Index(fields=["service", "price"]),
        ]

    def __str__(self) -> str:
        return f"{self.hospital.name} - {self.service.name} : {self.price}"
