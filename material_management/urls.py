from django.urls import path
from . import views

urlpatterns = [
    path('material_management/', views.material_management_home, name='material_management_home'),


]
