from django.db import models

class Product(models.Model):
    MEASUREMENT_CHOICES = [
        ('box', 'Box'),
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('packet', 'Packet'),
        ('litre', 'Litre'),
        ('piece', 'Piece'),
        # Add any other units needed
    ]

    product_code = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=100)
    batch = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    buying_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    measurement_unit = models.CharField(max_length=10, choices=MEASUREMENT_CHOICES, default='piece')  # New field
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('blocked', 'Blocked')], default='blocked')
    upload_date = models.DateField(auto_now_add=True)
    expire_date = models.DateField()

    def __str__(self):
        return f"{self.product_name} - {self.product_code}"
