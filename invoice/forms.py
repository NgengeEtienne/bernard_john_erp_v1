from django import forms
from django.forms import formset_factory

from .models import *
from customer.models import *
from product.models import *
from django_selectize import forms as s2forms


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'customer',
            'created',
            'sales_session',
            'invoice_total',
        ]
  
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control',
                'id': 'invoice_customer_name',
                'name': 'invoice_customer_name',
                'placeholder': 'Select Customer',
                'required': 'required',  # Make the field required
            }),

            'created': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'invoice_date',
                'placeholder': 'Enter date create',
                'type': 'date',
                'name': 'invoice_date',
            }),
 
            'sales_session': forms.Select(attrs={
                'class': 'form-control',
                'id': 'invoice_sales_session',
                'name': 'invoice_sales_session',
                'placeholder': 'Select Session',
                'required': 'required',  # Make the field required
            }),
            'invoice_total': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'hinvoice_total',
                'placeholder': '0',
                'type': 'hidden',
                'required': 'required',  # Make the field required
                'min': '1',  # Set the minimum value to 1
            }),

        }


class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = [
            'sales_person',
            'product',
            'quantity',
            'price',
            'discount_price',
            'discount_value',
        ]
        widgets = {

          'sales_person': forms.Select(attrs={
                'class': 'form-control',
                'id': 'sales_person',
                'placeholder': 'Name of the Vendor',
                'required': 'required',  # Make the field required
                'style': 'width: 116px;',  # Inline CSS for width
            }),


            'product': forms.Select(attrs={
                'class': 'form-control',  # Bootstrap form-select and form-control classes
                'id': 'invoice_detail_product',  # Keep the ID if necessary for JavaScript
                'placeholder': 'Select product...',
                'required': 'required',  # Make the field required
                'min': '0',  # Set the minimum value to 0
                'width':'40px',
            }),
 

            'quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_qty',
                'placeholder': '0',
                'type': 'number',
                'required': 'required',  # Make the field required
                'min': '1',  # Set the minimum value to 0
            }),

            'price': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_price',
                'placeholder': '0',
                'type': 'number',
                'required': 'required',  # Make the field required
                'min': '0',
                'readonly':'readonly',
            }),

            'discount_price': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_discount_price',
                'placeholder': '0',
                'type': 'number',
                'min': '0',
            }),
            'discount_value': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_discount_value',
                'placeholder': '0',
                'type': 'number',
                'min': '0',
                'readonly':'readonly',
            })

            
        }


		
InvoiceDetailFormSet = formset_factory(InvoiceDetailForm, extra=1)
