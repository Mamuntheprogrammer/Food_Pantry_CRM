from django.db import models

# Create your models here.
class Vendor(models.Model):
    vendor_number = models.CharField(max_length=50, unique=True)
    vendor_name = models.CharField(max_length=200)
    vendor_address = models.TextField()
    vendor_phone_number = models.CharField(max_length=15)
    vendor_email = models.EmailField()

    def __str__(self):
        return f"{self.vendor_name} ({self.vendor_number})"