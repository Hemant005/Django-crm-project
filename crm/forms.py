from django import forms
from .models import Client,Product,Opportunity,Invoice,Shipping_Receipt
from django.forms.widgets import DateInput


class Product_Form(forms.ModelForm):
    class Meta:
        model=Product
        fields=['product_name','product_qty','cost_price']

class Client_Form(forms.ModelForm):
    class Meta:
        model=Client
        fields=['name', 'company', 'email', 'phone', 'address']

class Opportunity_Form(forms.ModelForm):
    class Meta:
        model=Opportunity
        fields=['client', 'opportunity_name', 'estimated_value', 'requirement', 'estimated_qty', 'status']

class Invoice_Form(forms.ModelForm):
    class Meta:
        model=Invoice
        fields = ['client', 'opportunity','product','quantity', 'payment_date', 'payment_method', 'status']  # Exclude 'added_by' and 'date'
        widgets = {
            'payment_date': DateInput(attrs={'type': 'date'}),
        }

class Shipping_Form(forms.ModelForm):
    class Meta:
        model=Shipping_Receipt
        fields = ['client', 'delivery_address', 'delivery_status','opportunity','product','quantity']  # Exclude 'added_by' and 'date'
        