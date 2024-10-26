from django.shortcuts import render, redirect

# Create your views here.
def dashboard_home(request):
    return render(request, 'dashboard/home.html')