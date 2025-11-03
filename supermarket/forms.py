# bakery/forms.py
from django import forms
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django import forms
from .models import SupermarketCustomer, SupermarketProductCategory

class SupermarketCustomerForm(forms.ModelForm):
    class Meta:
        model = SupermarketCustomer
        fields = [
            'customer_name',
            'customer_type',
            'company_name',
            'company_box',
            'area',
            'quarter',
            'street',
            'street_location',
            'address',
            'city',
            'region',
            'phone',
            'email',
            'account_photo',
        ]

 

class SupermarketProductCategoryForm(forms.ModelForm):
    class Meta:
        model = SupermarketProductCategory
        fields = ['category_name', 'sub_department']  # Add fields you want in your form
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'sub_department': forms.Select(attrs={'class': 'form-control'}),
        }

 
from django import forms
from .models import SupermarketInvoice, SupermarketInvoiceDetail

class SupermarketInvoiceForm(forms.ModelForm):
    class Meta:
        model = SupermarketInvoice
        fields = [
            'customer',
            'created',
            'sales_session',
            'invoice_total',
            'sales_person',
            'status'
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
            'sales_person': forms.Select(attrs={
                'class': 'form-control',
                'id': 'sales_person',
                'placeholder': 'Name of the Vendor',
                'required': 'required',  # Make the field required
            }),
             'status': forms.Select(attrs={
                'class': 'form-control',
                'id': 'status',
                'placeholder': 'Status',
                'required': 'required',  # Make the field required
            }),

        }


class SupermarketInvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = SupermarketInvoiceDetail
        fields = [
            'product',
            'quantity',
            'price',
            'discount_price',
            'discount_value',
        ]
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',  # Bootstrap form-select and form-control classes
                'id': 'invoice_detail_product',  # Keep the ID if necessary for JavaScript
                'placeholder': 'Select product...',
                'required': 'required',  # Make the field required
                'width':'60px',
            }),
 

            'quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_qty',
                'placeholder': '0',
                'type': 'number',
                'required': 'required',  # Make the field required
                'min': '1',  # Set the minimum value to 0
                'style': 'width: 60px;'
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


		
SupermarketInvoiceDetailFormSet = formset_factory(SupermarketInvoiceDetailForm, extra=1)



from .models import SupermarketPurchase, SupermarketPurchaseItems

class SupermarketPurchaseForm(forms.ModelForm):
    class Meta:
        model = SupermarketPurchase
        fields = [
            'employee',
            'supplier_name',
            'created',
            'department',
            'recieved_date',
            'ordered_date'
        ]

  
        widgets = {
            'employee': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'purchase_employee',
                'placeholder': 'Enter Employee Name',
                'required': 'required',  # Make the field required
            }),

            'supplier_name': forms.Select(attrs={
                'class': 'form-control',
                'id': 'purchase_supplier_name',
                'placeholder': 'Select Supplier',
                'required': 'required',  # Make the field required
            }),

            'created': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'purchase_created',
                'placeholder': 'Enter Date',
                'type': 'date',
                'name': 'purchase_created',
            }),
            'ordered_date': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'order_date',
                'placeholder': 'Enter Date',
                'type': 'date',
                'name': 'order_date',
            }),
            'recieved_date': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'recieved_date',
                'placeholder': 'Enter Date',
                'type': 'date',
                'name': 'recieved_date',
            }),
            'department': forms.Select(attrs={
                'class': 'form-control',
                'id': 'sales_person',
                'placeholder': 'Name of the Vendor',
                'required': 'required',  # Make the field required
            }),

        }


class SupermarketPurchaseItemsForm(forms.ModelForm):
    class Meta:
        model = SupermarketPurchaseItems
        fields = [
            'created',
            # 'department',
            'product',
            # 'recieved_date',
            # 'ordered_date',  # Added missing comma here
            'quantity',
            'unit_cost_price',
            'unit_selling_price',
            'discount_price',
            'discount_value',
        ]
        widgets = {
            # 'ordered_date': forms.DateInput(attrs={
            #     'class': 'form-control',
            #     'id': 'order_date',
            #     'placeholder': 'Enter Date',
            #     'type': 'date',
            #     'name': 'order_date',
            # }),
            
            # 'recieved_date': forms.DateInput(attrs={
            #     'class': 'form-control',
            #     'id': 'recieved_date',
            #     'placeholder': 'Enter Date',
            #     'type': 'date',
            #     'name': 'recieved_date',
            # }),
            
            'product': forms.Select(attrs={
                'class': 'form-control',  # Bootstrap form-select and form-control classes
                'id': 'invoice_detail_product',  # Keep the ID if necessary for JavaScript
                'placeholder': 'Select product...',
                'required': 'required',  # Make the field required
            }),

            'quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_qty',
                'placeholder': '0',
                'type': 'number',
                'required': 'required',  # Make the field required
                'min': '1',  # Set the minimum value to 1
            }),

            'unit_cost_price': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_price',
                'placeholder': '0',
                'type': 'number',
                'required': 'required',  # Make the field required
                'min': '0',
            }),
            
            'unit_selling_price': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_price',
                'placeholder': '0',
                'type': 'number',
                'required': 'required',  # Make the field required
                'min': '0',
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
                'readonly': 'readonly',  # Read-only field
            }),
        }

# FormSet for multiple SupermarketPurchaseItems entries
SupermarketPurchaseItemsFormSet = forms.modelformset_factory(
    SupermarketPurchaseItems,
    form=SupermarketPurchaseItemsForm,
    extra=1,  # Define how many extra blank forms you want
)