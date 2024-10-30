from django.urls import path
from . import views

urlpatterns = [
    path('stock_management/', views.stock_management_home, name='stock_management_home'),
    path('stock_management/block/<int:product_id>/', views.block_product, name='block_product'),
    path('stock_management/activate/<int:product_id>/', views.activate_product, name='activate_product'),
    path('stock_management/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('stock_management/delete/<int:product_id>/', views.delete_product, name='delete_product'),


]

