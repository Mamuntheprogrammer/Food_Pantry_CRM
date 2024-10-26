from django.shortcuts import render, redirect

# Create your views here.
def order_management_home(request):
    return render(request, 'order_management/home.html')