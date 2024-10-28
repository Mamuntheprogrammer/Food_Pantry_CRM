from django.urls import path
from . import views

urlpatterns = [
    path('order_management/', views.order_management_home, name='order_management_home'),
    path('approve_order/<int:order_id>/', views.approve_order, name='approve_order'),  
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'), 
    
]
