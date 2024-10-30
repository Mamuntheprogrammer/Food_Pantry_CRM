from django import forms

class StockUploadForm(forms.Form):
    file = forms.FileField()
