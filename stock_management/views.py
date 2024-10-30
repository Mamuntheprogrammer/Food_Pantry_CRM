

import pandas as pd
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import Product
from .forms import StockUploadForm



# # Create your views here.
# def stock_management_home(request):
#     return render(request, 'stock_management/home.html')


def stock_management_home(request):
    # Fetch all products, total count, and unique product count
    products = Product.objects.all()
    total_count = products.count()
    unique_products = products.values('product_code').distinct().count()

    if request.method == 'POST':
        form = StockUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            try:
                df = pd.read_excel(file)
                
                # Print column names to debug
                print("Excel columns:", df.columns.tolist())
                
                for _, row in df.iterrows():
                    # Use .get() and .strip() to handle any extra spaces
                    Product.objects.update_or_create(
                        product_code=row.get('Product Code', '').strip(),
                        defaults={
                            'product_name': row.get('Product Name', '').strip(),
                            'batch': row.get('Batch', '').strip(),
                            'quantity': row.get('Quantity', 0),
                            'buying_price_per_unit': row.get('Buying Price per Unit', 0.0),
                            'selling_price_per_unit': row.get('Selling Price per Unit', 0.0),
                            'measurement_unit': row.get('Measurement Unit', 'pcs').strip(),
                            'expire_date': row.get('Expire Date', None),
                            'status': 'active'
                        }
                    )
                messages.success(request, "Stock uploaded successfully.")
            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
            return redirect('stock_management_home')
    else:
        form = StockUploadForm()

    return render(request, 'stock_management/home.html', {
        'form': form,
        'products': products,
        'total_count': total_count,
        'unique_products': unique_products
    })





def block_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.status = 'blocked'
    product.save()
    messages.success(request, f'Product {product.product_name} has been blocked.')
    return redirect('stock_management_home')

def activate_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.status = 'active'
    product.save()
    messages.success(request, f'Product {product.product_name} has been activated.')
    return redirect('stock_management_home')

def edit_product(request, product_id):
    # Implement the logic for editing the product
    pass

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, f'Product {product.product_name} has been deleted.')
    return redirect('stock_management_home')