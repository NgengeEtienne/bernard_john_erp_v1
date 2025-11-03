# bar/forms.py
from django import forms
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django import forms
from django.forms import modelformset_factory

from .models import BarSupplier, BarProductCategory

class BarSupplierForm(forms.ModelForm):
    class Meta:
        model = BarSupplier
        fields = [
            'supplier_name',
            'supplier_type',
            'company_name',
            
            'slug',
            'address',
            'city',
            'region',
            'phone1',
            'phone2',
            # 'account_photo',
        ]

 

class BarProductCategoryForm(forms.ModelForm):
    class Meta:
        model = BarProductCategory
        fields = ['category_name']  # Add fields you want in your form
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'})
        }


# from django import forms
# from .models import BarInvoice, BarInvoiceDetail

# class BarInvoiceForm(forms.ModelForm):
#     class Meta:
#         model = BarInvoice
#         fields = [
#             'customer',
#             'created',
#             'sales_session',
#             'invoice_total',
#             'sales_person',
#         ]
  
#         widgets = {
#             'customer': forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'invoice_customer_name',
#                 'name': 'invoice_customer_name',
#                 'placeholder': 'Select Supplier',
#                 'required': 'required',  # Make the field required
#             }),

#             'created': forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'id': 'invoice_date',
#                 'placeholder': 'Enter date create',
#                 'type': 'date',
#                 'name': 'invoice_date',
#             }),
 
#             'sales_session': forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'invoice_sales_session',
#                 'name': 'invoice_sales_session',
#                 'placeholder': 'Select Session',
#                 'required': 'required',  # Make the field required
#             }),
#             'invoice_total': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'hinvoice_total',
#                 'placeholder': '0',
#                 'type': 'hidden',
#                 'required': 'required',  # Make the field required
#                 'min': '1',  # Set the minimum value to 1
#             }),
#             'sales_person': forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'sales_person',
#                 'placeholder': 'Name of the Vendor',
#                 'required': 'required',  # Make the field required
#             }),

#         }


# class BarInvoiceDetailForm(forms.ModelForm):
#     class Meta:
#         model = BarInvoiceDetail
#         fields = [
#             'product',
#             'quantity',
#             'price',
#             'discount_price',
#             'discount_value',
#         ]
#         widgets = {
#             'product': forms.Select(attrs={
#                 'class': 'form-control',  # Bootstrap form-select and form-control classes
#                 'id': 'invoice_detail_product',  # Keep the ID if necessary for JavaScript
#                 'placeholder': 'Select product...',
#                 'required': 'required',  # Make the field required
#                 'width':'150px',
#             }),
 

#             'quantity': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'invoice_detail_qty',
#                 'placeholder': '0',
#                 'type': 'number',
#                 'required': 'required',  # Make the field required
#                 'min': '1',  # Set the minimum value to 0
#                 'style': 'width: 150px;',
#                 "inputType": "number",
#                 "step": 1
#             }),

#             'price': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'invoice_detail_price',
#                 'placeholder': '0',
#                 'type': 'number',
#                 'required': 'required',  # Make the field required
#                 'min': '0',
#                 'readonly':'readonly',
#                 'width':'50px',
#             }),

#             'discount_price': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'invoice_discount_price',
#                 'placeholder': '0',
#                 'type': 'number',
#                 'min': '0',
#                 'width':'50px',
#             }),
#             'discount_value': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'invoice_discount_value',
#                 'placeholder': '0',
#                 'type': 'number',
#                 'min': '0',
#                 'readonly':'readonly',
#             })

            
#         }


		
# BarInvoiceDetailFormSet = formset_factory(BarInvoiceDetailForm, extra=1)



from .models import BarPurchase, BarPurchaseItems

class BarPurchaseForm(forms.ModelForm):
    class Meta:
        model = BarPurchase
        fields = [
            'employee',
            'supplier_name',
            'created',
            'sub_department',
            'status',
            # 'ordered_date'
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
            'status': forms.Select(attrs={
                'class': 'form-control',
                'id': 'status',
                'placeholder': 'Enter Date',
                'type': 'datetime-local',
                'name': 'status',
            }),
            # 'recieved_date': forms.DateTimeInput(attrs={
            #     'class': 'form-control',
            #     'id': 'recieved_date',
            #     'placeholder': 'Enter Date',
            #     'type': 'datetime-local',
            #     'name': 'recieved_date',
            # }),
            'sub_department': forms.Select(attrs={
                'class': 'form-control',
                'id': 'sales_person',
                'placeholder': 'Name of the Vendor',
                'required': 'required',  # Make the field required
            }),

        }


class BarPurchaseItemsForm(forms.ModelForm):
    class Meta:
        model = BarPurchaseItems
        fields = [
            'product_name',
            'quantity',
            'selling_price',
            'discount_amount',
            'discount_value',
        ]
        widgets = {
            'product_name': forms.Select(attrs={
                'class': 'form-control',  # Bootstrap form-select and form-control classes
                'id': 'invoice_detail_product',  # Keep the ID if necessary for JavaScript
                'placeholder': 'Select product...',
                'required': 'required',  # Make the field required
                #'width':'60px',
            }),
 

            'quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_qty',
                'placeholder': '0',
                'type': 'number',
                'required': 'required',  # Make the field required
                'min': '1',  # Set the minimum value to 0
                'width':'60px',
                "inputType": "number",
                "step": 1
            }),

            'selling_price': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_price',
                'placeholder': '0',
                'type': 'number',
                'required': 'required',  # Make the field required
                'min': '0',
                'width':'60px',
            }),

            'discount_amount': forms.TextInput(attrs={
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

# FormSet for multiple BarPurchaseItems entries
BarPurchaseItemsFormSet = forms.modelformset_factory(
    BarPurchaseItems,
    form=BarPurchaseItemsForm,
    extra=1,
)



#--------------------------- Production --------------------------------#
# class BarProductionForm(forms.ModelForm):
#     class Meta:
#         model = BarProduction
#         fields = [
#             'created_at',
#             'production_id',
#             'department',
#             'sub_department',
#             'session',
#             'supervisor',
#             'stock_supervisor',
#             'mixture_number',
#         ]
  
#         widgets = {
#             'created_at': forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'id': 'production_created_at',
#                 'placeholder': 'Enter Production Date',
#                 'type': 'date',
#                 'name': 'production_created_at',
#             }),

#             'department': forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'production_department',
#                 'placeholder': 'Select Department',
#                 'required': 'required',
#             }),
 
#             'sub_department': forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'production_sub_department',
#                 'placeholder': 'Select Sub-Department',
#                 'required': 'required',
#             }),

#             'mixture_number': forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'production_session',
#                 'placeholder': 'Select Session',
#                 'required': 'required',
#             }),
            
#             'session': forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'production_session',
#                 'placeholder': 'Select Session',
#                 'required': 'required',
#             }),

#             'supervisor': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'production_supervisor',
#                 'placeholder': 'Name of the Supervisor',
#                 'required': 'required',
#             }),
            
#             'stock_supervisor': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'production_stock_supervisor',
#                 'placeholder': 'Name of the Stock Supervisor',
#                 'required': 'required',
#             }),
            
            
#         }

# class BarRawMaterialUsageForm(forms.ModelForm):
#     class Meta:
#         model = BarRawMaterialUsage
#         fields = [
#             'raw_material',
#             'qty',
#             'unit_cost_price'


#         ]
#         widgets = {
            
            
#             'raw_material': forms.Select(attrs={
#                 'class': 'form-control ',
#                 'id': 'raw_material',
#                 'placeholder': 'Select Raw Material...',
#                 'required': 'required',
#                 'width':'60px',
#             }),
 
#             'qty': forms.TextInput(attrs={
#                 'class': 'form-control ',
#                 'id': 'qty',
#                 'placeholder': '0',
#                 'type': 'number',
#                 'required': 'required',
#                 'min': '0',
#                 "inputType": "number",
#                 "step": 1
#                 # 'style': 'width:300px;',
#             }),
            
#             'unit_cost_price': forms.TextInput(attrs={
#                 'class': 'form-control ',
#                 'id': 'qty',
#                 'placeholder': '0',
#                 'type': 'number',
#                 'required': 'required',
#                 'min': '0',
#                 'readonly':'readonly'
#                 #'style': 'width:300px;',
#             }),
#         }

# BarRawMaterialUsageFormSet = modelformset_factory(BarRawMaterialUsage, 
#                                                      form=BarRawMaterialUsageForm, extra=1)
#--------------------------- / Production --------------------------------#




from .models import BarInventory, BarInventoryItems

class BarInventoryForm(forms.ModelForm):
    class Meta:
        model = BarInventory
        fields = ['employee', 'created','description']
        widgets={
             'description':forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'description',
                'placeholder': 'description ',
                'cols': 50,  # Specify the width in terms of character columns
                'rows': 1,   # Optionally, specify the number of rows
                'required': 'required',  # Make the field required
            }),
            'employee':forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'employee',
                'placeholder': 'Employee name',
                'required': 'required',  # Make the field required
            }),
            'created':forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'created',
                'placeholder': 'created',
                'type': 'date',
                'required': 'required',  # Make the field required
            }),
        }

class BarInventoryItemsForm(forms.ModelForm):
    class Meta:
        model = BarInventoryItems
        fields = ['status', 'product_name', 'quantity', 'selling_price']
        widgets={
            'status':forms.Select(attrs={
                'class': 'form-control',
                'id': 'status',
                'placeholder': 'status',
                'required': 'required',  # Make the field required
            }),
            'product_name':forms.Select(attrs={
                'class': 'form-control',
                'id': 'raw_material-product',
                'placeholder': 'Name of the Product',
                'required': 'required',  # Make the field required
            }),
            'quantity':forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'quantity',
                'placeholder': 'Quantity',
                'required': 'required',  # Make the field required
                "inputType": "number",
                "step": 1
            }),
            'selling_price':forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'price',
                'placeholder': 'price',
                'required': 'required',
                 'readonly':'readonly'  # Make the field required
            }),
        }



BarInventoryItemsFormSet = forms.modelformset_factory(
    BarInventoryItems,
    form=BarInventoryItemsForm,
    extra=1,
)



# from .models import BarProductionOutput  # Replace with your actual model name

# class BarProductionOutputForm(forms.ModelForm):
#     class Meta:
#         model = BarProductionOutput  # Replace with your actual model name
#         fields = [
           
#             'output_category',
#             'mixture_number',
#             'tag',
#             'product',
#             'qty',
#             'product_price',
#             'value',
#         ]
#         widgets = {
#     'output_category': forms.Select(attrs={
#         'class': 'form-control ',
#         'id': 'output_category',  # Adding id attribute
#         'placeholder': 'Select Output Category',
#     }),
#     'mixture_number': forms.Select(attrs={
#         'class': 'form-control ',
#         'id': 'mixture_number',  # Adding id attribute
#         'placeholder': 'Select Mixture Number',
#     }),
#     'tag': forms.Select(attrs={
#         'class': 'form-control ',
#         'id': 'tag',  # Adding id attribute
#         'placeholder': 'Select Tag',
#     }),
#     'product': forms.Select(attrs={
#         'class': 'form-control ',
#         'id': 'product',  # Adding id attribute
#         'placeholder': 'Select Product',
#     }),
#     'qty': forms.NumberInput(attrs={
#         'class': 'form-control ',
#         'id': 'qty',  # Adding id attribute
#         'placeholder': 'Enter Quantity',
#         "inputType": "number",
#          "step": 1
#     }),
#     'product_price': forms.NumberInput(attrs={
#         'class': 'form-control ',
#         'id': 'product_price',  # Adding id attribute
#         'placeholder': 'Enter Price',
#         'readonly':'readonly'
#     }),
#     'value': forms.NumberInput(attrs={
#         'class': 'form-control ',
#         'id': 'value',  # Adding id attribute
#         'placeholder': 'Enter Output Value',
#     }),
# }

# BarProductionOutputFormset = forms.modelformset_factory(
#     BarProductionOutput,
#     form=BarProductionOutputForm,
#     extra=1,
# )