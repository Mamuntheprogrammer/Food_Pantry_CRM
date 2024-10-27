
from django.db import models
from django.contrib.auth.models import User
import uuid

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    stock_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.name} (Stock: {self.stock_quantity})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    delivery_date = models.DateField(null=True, blank=True)
    delivery_address = models.CharField(max_length=255, blank=True)
    note = models.TextField(blank=True)
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Delivered', 'Delivered')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_number} - {self.user.username} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity} for Order {self.order.order_number}"

