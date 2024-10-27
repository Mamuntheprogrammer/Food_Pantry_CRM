
# Register your models here.
from django.contrib import admin

from .models import *

admin.site.register(PasswordReset)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)