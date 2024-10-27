from django import forms
from django.contrib.auth.models import User
from .models import Order, Product, OrderItem

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']   # Add any other fields as needed





# class OrderForm(forms.ModelForm):
#     products = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), widget=forms.CheckboxSelectMultiple)
    
#     class Meta:
#         model = Order
#         fields = ['products', 'delivery_date', 'delivery_address', 'note']
    
#     def __init__(self, *args, **kwargs):
#         super(OrderForm, self).__init__(*args, **kwargs)
#         # Create quantity fields for each product
#         if 'products' in self.data:
#             try:
#                 products = Product.objects.filter(id__in=self.data.getlist('products'))
#                 for product in products:
#                     self.fields[f'quantity_{product.id}'] = forms.IntegerField(min_value=1, initial=1)
#             except (ValueError, TypeError):
#                 pass  # Handle invalid input

# from django import forms
# from .models import Order, Product

class OrderForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    delivery_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-field'})  # Ensure it’s a date field
    )

    class Meta:
        model = Order
        fields = ['products', 'delivery_date', 'delivery_address', 'note']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # Create quantity fields for each selected product
        if 'products' in self.data:
            try:
                products = Product.objects.filter(id__in=self.data.getlist('products'))
                for product in products:
                    self.fields[f'quantity_{product.id}'] = forms.IntegerField(
                        min_value=1,
                        initial=1,
                        label=f"Quantity for {product.name}"  # Optional: Label for clarity
                    )
            except (ValueError, TypeError):
                pass  # Handle invalid input

    def clean(self):
        cleaned_data = super().clean()
        selected_products = cleaned_data.get('products')
        quantities = {}
        
        # Validate quantities for each selected product
        for product in selected_products:
            quantity = cleaned_data.get(f'quantity_{product.id}')
            if quantity is None or quantity <= 0:
                self.add_error(f'quantity_{product.id}', f"Please enter a valid quantity for {product.name}.")
            elif quantity > product.stock_quantity:
                self.add_error(f'quantity_{product.id}', f"Only {product.stock_quantity} in stock for {product.name}.")
            quantities[product] = quantity

        cleaned_data['quantities'] = quantities
        return cleaned_data

    def save(self, commit=True):
        order = super(OrderForm, self).save(commit=False)
        if commit:
            order.save()
            for product, quantity in self.cleaned_data['quantities'].items():
                OrderItem.objects.create(order=order, product=product, quantity=quantity)
        return order

