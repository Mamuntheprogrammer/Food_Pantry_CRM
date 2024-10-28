from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from user_management.models import Order
from django.utils import timezone
from django.contrib import messages

def order_management_home(request):
    # Count total orders, approved orders, and pending orders
    total_orders = Order.objects.count()
    approved_orders = Order.objects.filter(status="Approved").count()
    pending_orders = Order.objects.filter(status="Pending").count()
    
    # Retrieve the last 10 orders, with optional date filter
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    orders = Order.objects.all().order_by('-created_at')[:10]

    if start_date and end_date:
        orders = orders.filter(created_at__date__range=[start_date, end_date])
    
    context = {
        "total_orders": total_orders,
        "approved_orders": approved_orders,
        "pending_orders": pending_orders,
        "orders": orders,
        "start_date": start_date,
        "end_date": end_date
    }
    return render(request, "order_management/home.html", context)

def approve_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = "Approved"
    order.save()
    messages.success(request, "Order approved successfully.")
    return redirect("order_management_home")

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, "Order deleted successfully.")
    return redirect("order_management_home")
