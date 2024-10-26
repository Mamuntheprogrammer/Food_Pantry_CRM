from django.urls import path
from . import views

urlpatterns = [
    path('vendor_management/', views.vendor_management_home, name='vendor_management_home'),


]
