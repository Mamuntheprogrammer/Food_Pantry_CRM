from django.shortcuts import render, redirect

# Create your views here.
def vendor_management_home(request):
    return render(request, 'vendor_management/home.html')