
from django.shortcuts import render, redirect
from django.contrib import messages


# Create your views here.
def order_management_home(request):
    return render(request, 'order_management/home.html')


