from django.shortcuts import render, redirect

# Create your views here.
def material_management_home(request):
    return render(request, 'material_management/home.html')