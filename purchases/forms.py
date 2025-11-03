from django import forms
from django.forms import formset_factory

from .models import *
from customer.models import *
from inventory.models import *
from django_selectize import forms as s2forms

class InvoicesForm(forms.ModelForm):
    class Meta:
        model = Invoices
        fields = [
            'supplier',
            'created',
            'sub_department',
            'employee',
        ]
 
        widgets = {
            'supplier': forms.Select(attrs={
                'class': 'form-control',
                'id': 'invoice_supplier_name',
                'name': 'invoice_supplier_name',
                'required': 'required',
            }),

            'created': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'invoice_date',
                'placeholder': 'Enter date create',
                'type': 'date',
                'name': 'invoice_date',
            }),

            'sub_department': forms.Select(attrs={
                'class': 'form-control',
                'id': 'invoice_sales_session',
                'name': 'invoice_sales_session',
            }),

            'employee': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'sales_person',
                'placeholder': 'Employee Name',
            }),
        }


class InvoicesDetailForm(forms.ModelForm):
    class Meta:
        model = InvoicesDetail
        fields = [
            'product',
            'quantity',
            'price',
            'discount_price',
            'discount_value',
        ]
        widgets = {

            'product': forms.Select(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_product',
            }),

            'quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_qty',
                'placeholder': '0',
                'type': 'number',
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

InvoicesDetailFormSet = formset_factory(InvoicesDetailForm, extra=1)