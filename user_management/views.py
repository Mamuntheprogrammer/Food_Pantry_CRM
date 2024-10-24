from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from . import models



def home(request):
    return render(request,'user_management\home.html')



def signup(request):
    if request.method =="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_err = False

        if User.objects.filter(username=username).exists():
            user_data_err = True
            messages.error(request,"Username Already Exists")

        if User.objects.filter(email=email).exists():
            user_data_err = True
            messages.error(request,"Email Already Exists")

        if len(password)<6:
            user_data_err = True
            messages.error(request,"Password Must Be atleast 6 Characters")
        
        if user_data_err:
            return redirect('signup')
        
        if not user_data_err:
            new_user = User.objects.create_user(
                first_name =first_name,
                last_name = last_name,
                username = username,
                email = email,
                password = password,
            )
            messages.success(request, "Accound Created ! Please Login Now")
            return redirect('home')
        

        



    return render(request,'user_management\signup.html')