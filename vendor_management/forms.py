from django import forms
from .models import Vendor



class VendorUploadForm(forms.Form):
    file = forms.FileField()



class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_number', 'vendor_name', 'vendor_address', 'vendor_phone_number', 'vendor_email']
        widgets = {
            'vendor_address': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
        }