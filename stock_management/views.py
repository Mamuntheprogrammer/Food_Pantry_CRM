from django.shortcuts import render, redirect

# Create your views here.
def stock_management_home(request):
    return render(request, 'stock_management/home.html')