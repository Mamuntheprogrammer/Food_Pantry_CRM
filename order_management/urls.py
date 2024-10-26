from django.urls import path
from . import views

urlpatterns = [
    path('order_management/', views.order_management_home, name='order_management_home'),


]
