import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from stock_management.models import Product
from .models import Vendor
from .forms import VendorUploadForm,VendorForm
# Vendor Management Home View
def vendor_management_home(request):
    # Fetch all vendors and products linked to vendors
    vendors = Vendor.objects.all()
    total_vendors = vendors.count()

    if request.method == 'POST':
        form = VendorUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            try:
                df = pd.read_excel(file)
                
                # Print column names to debug
                print("Excel columns:", df.columns.tolist())
                
                for _, row in df.iterrows():
                    # Use .get() and .strip() to handle any extra spaces
                    Vendor.objects.update_or_create(
                        vendor_number=row.get('Vendor Number', '').strip(),
                        defaults={
                            'vendor_name': row.get('Vendor Name', '').strip(),
                            'vendor_address': row.get('Vendor Address', '').strip(),
                            'vendor_phone_number': row.get('Vendor Phone', '').strip(),
                            'vendor_email': row.get('Vendor Email', '').strip(),
                        }
                    )
                messages.success(request, "Vendors uploaded successfully.")
            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
            return redirect('vendor_management_home')
    else:
        form = VendorUploadForm()

    return render(request, 'vendor_management/home.html', {
        'form': form,
        'vendors': vendors,
        'total_vendors': total_vendors,
    })

# Create Vendor
def create_vendor(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vendor added successfully.")
            return redirect('vendor_management_home')
    else:
        form = VendorForm()

    return render(request, 'vendor_management/vendor_form.html', {'form': form})

# Edit Vendor
def edit_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, f"Vendor {vendor.vendor_name} has been updated.")
            return redirect('vendor_management_home')
    else:
        form = VendorForm(instance=vendor)
    
    return render(request, 'vendor_management/vendor_form.html', {'form': form, 'vendor': vendor})

# Delete Vendor
def delete_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor.delete()
    messages.success(request, f"Vendor {vendor.vendor_name} has been deleted.")
    return redirect('vendor_management_home')

# Link a Product to a Vendor
def assign_vendor_to_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product {product.product_name} has been assigned to the vendor.")
            return redirect('vendor_management_home')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'vendor_management/assign_vendor_to_product.html', {'form': form, 'product': product})
