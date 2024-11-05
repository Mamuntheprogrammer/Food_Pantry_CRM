from django.urls import path
from . import views

urlpatterns = [
    # Vendor Management
    path('vendor_management/', views.vendor_management_home, name='vendor_management_home'),
    path('vendor_management/create/', views.create_vendor, name='create_vendor'),
    path('vendor_management/edit/<int:vendor_id>/', views.edit_vendor, name='edit_vendor'),
    path('vendor_management/delete/<int:vendor_id>/', views.delete_vendor, name='delete_vendor'),
    
    # Product Management (Linking products to vendors)
    path('product/assign_vendor/<int:product_id>/', views.assign_vendor_to_product, name='assign_vendor_to_product'),

    # Vendor Upload
    path('vendor_management/upload/', views.vendor_management_home, name='vendor_upload'),  # Reusing the upload functionality
]
