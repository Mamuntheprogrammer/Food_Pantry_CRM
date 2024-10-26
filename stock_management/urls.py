from django.urls import path
from . import views

urlpatterns = [
    path('stock_management/', views.stock_management_home, name='stock_management_home'),


]
