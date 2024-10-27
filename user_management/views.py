from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import PasswordReset
from .forms import UpdateProfileForm
from .forms import OrderForm
import random
import string
from django.db.models import Max
from .models import Order,OrderItem


def home(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect('adprofile')
            return redirect('profile')
        else:
            messages.error(request, "Invalid Username Or Password")
            return redirect('home')

    return render(request, 'user_management/home.html')


def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_err = False

        if User.objects.filter(username=username).exists():
            user_data_err = True
            messages.error(request, "Username Already Exists")

        if User.objects.filter(email=email).exists():
            user_data_err = True
            messages.error(request, "Email Already Exists")

        if len(password) < 6:
            user_data_err = True
            messages.error(request, "Password Must Be at least 6 Characters")

        if user_data_err:
            return redirect('signup')
        else:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            messages.success(request, "Account Created! Please Login Now")
            return redirect('home')
    return render(request, 'user_management/signup.html')


@login_required
def profile(request):
    user_orders = Order.objects.filter(user=request.user)
    return render(request, 'user_management/profile.html', {'user_orders': user_orders})

@login_required
def adprofile(request):
    return render(request, 'user_management/admin_profile.html')

def logoutview(request):
    logout(request)
    return redirect('home')


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UpdateProfileForm(instance=request.user)

    return render(request, 'user_management/update_profile.html', {'form': form})


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            email_body = f'Reset your password using the link below:\n\n{full_password_reset_url}'

            email_message = EmailMessage(
                'Reset your password',
                email_body,
                settings.EMAIL_HOST_USER,
                [email]
            )
            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

    return render(request, 'user_management/forgot_password.html')


def passwordResetSent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'user_management/password_reset_sent.html')
    else:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')




def resetPassword(request, reset_id):
    try:
        password_reset_instance = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('new_password1')
            confirm_password = request.POST.get('new_password2')

            passwords_have_error = False

            # Check for empty fields
            if not password or not confirm_password:
                passwords_have_error = True
                messages.error(request, 'Password fields cannot be empty')

            elif password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            elif len(password) < 6:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 6 characters long')

            # Check if the link has expired
            expiration_time = password_reset_instance.created_when + timezone.timedelta(minutes=10)
            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')
                password_reset_instance.delete()

            # If no errors, reset the password
            if not passwords_have_error:
                user = password_reset_instance.user
                user.set_password(password)
                user.save()
                password_reset_instance.delete()

                messages.success(request, 'Password has been reset. Please log in.')
                return redirect('home')

            # Redirect back if errors are found
            return redirect('reset-password', reset_id=reset_id)

    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

    return render(request, 'user_management/reset_password.html')


 # Adjust the import based on your model's location

def generate_order_number():
    """Generate a new order number based on the last order number."""
    last_order = Order.objects.aggregate(Max('order_number'))  # Adjust field name if needed
    last_order_number = last_order['order_number__max']

    if last_order_number is None:
        new_order_number = 1  # Start from 1 if no orders exist
    else:
        new_order_number = int(last_order_number) + 1  # Increment last order number

    return str(new_order_number)  # Convert it back to string




@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            selected_products = form.cleaned_data['products']
            insufficient_stock = []
            quantities = {f'quantity_{product.id}': request.POST.get(f'quantity_{product.id}') for product in selected_products}

            # Check stock and create order
            for product in selected_products:
                quantity = int(quantities[f'quantity_{product.id}'])
                if product.stock_quantity < quantity:
                    insufficient_stock.append(product.name)
                else:
                    # Create order and order items
                    order = form.save(commit=False)
                    order.user = request.user
                    order.order_number = generate_order_number()  # Implement this function
                    order.save()
                    OrderItem.objects.create(order=order, product=product, quantity=quantity)
                    product.stock_quantity -= quantity  # Decrement stock by the quantity ordered
                    product.save()

            if insufficient_stock:
                messages.error(request, f'Stock not available for: {", ".join(insufficient_stock)}')
                return redirect('create_order')

            messages.success(request, 'Order created successfully!')
            return redirect('profile')  # Redirect to profile after order creation
    else:
        form = OrderForm()
    return render(request, 'user_management/create_order.html', {'form': form})


def edit_order(request, id):
    order = get_object_or_404(Order, id=id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order updated successfully!')
            return redirect('profile')  # Redirect to the profile page
    else:
        form = OrderForm(instance=order)

    return render(request, 'user_management/edit_order.html', {'form': form, 'order': order})


def delete_order(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order deleted successfully!')
        return redirect('profile')  # Redirect to profile after deletion
    return render(request, 'user_management/delete_confirmation.html', {'order': order})