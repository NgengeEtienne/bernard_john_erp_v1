# wholesale/forms.py
from django import forms
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django import forms
from django.forms import modelformset_factory

from .models import WholesaleCustomer,WholesaleProductSubCategory

class WholesaleCustomerForm(forms.ModelForm):
    class Meta:
        model = WholesaleCustomer
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
            # 'account_photo',
        ]

 

class WholesaleProductCategoryForm(forms.ModelForm):
    class Meta:
        model = WholesaleProductSubCategory
        fields = ['sub_category_name']  # Add fields you want in your form
        widgets = {
            'sub_category_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'})
            # 'sub_department': forms.Select(attrs={'class': 'form-control'}),
        }


from django import forms
from .models import WholesaleInvoice, WholesaleInvoiceDetail

class WholesaleInvoiceForm(forms.ModelForm):
    class Meta:
        model = WholesaleInvoice
        fields = [
            'customer',
            'created',
            'status',
            'invoice_total',
            # 'sales_person',
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
 
            'status': forms.Select(attrs={
                'class': 'form-control',
                'id': 'status',
                'name': 'status',
                'placeholder': 'Select Status',
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
            # 'sales_person': forms.Select(attrs={
            #     'class': 'form-control',
            #     'id': 'sales_person',
            #     'placeholder': 'Name of the Vendor',
            #     'required': 'required',  # Make the field required
            # }),

        }


class WholesaleInvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = WholesaleInvoiceDetail
        fields = [
            'product',
            'quantity',
            'unit_selling_price',
            'discount_price',
            'discount_value',
            'sales_person',
            'delivery_man',
        ]
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',  # Bootstrap form-select and form-control classes
                'id': 'invoice_detail_product',  # Keep the ID if necessary for JavaScript
                'placeholder': 'Select product...',
                'required': 'required',  # Make the field required
                'width':'150px',
            }),
 

            'quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_qty',
                'placeholder': '0',
                'type': 'number',
                'required': 'required',  # Make the field required
                'min': '1',  # Set the minimum value to 0
                'style': 'width: 150px;',
                "inputType": "number",
                "step": 1
            }),

            'unit_selling_price': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_price',
                'placeholder': '0',
                'type': 'number',
                'required': 'required',  # Make the field required
                'min': '0',
                'readonly':'readonly',
                'width':'50px',
            }),

            'discount_price': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_discount_price',
                'placeholder': '0',
                'type': 'number',
                'min': '0',
                'width':'50px',
            }),
            'discount_value': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_discount_value',
                'placeholder': '0',
                'type': 'number',
                'min': '0',
                'readonly':'readonly',
            }),
            'sales_person': forms.Select(attrs={
                'class': 'form-control',
                'id': 'sales_person',
                'placeholder': 'Name of the Vendor',
                'required': 'required',  # Make the field required
            }),
            'delivery_man': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'delivery_man',
                'placeholder': 'Delivery man',
                'required': 'required',  # Make the field required
            }),
            
        }


		
WholesaleInvoiceDetailFormSet = formset_factory(WholesaleInvoiceDetailForm, extra=1)



from .models import WholesalePurchase, WholesalePurchaseItems

class WholesalePurchaseForm(forms.ModelForm):
    class Meta:
        model = WholesalePurchase
        fields = [
            'employee',
            'supplier_name',
            'created',
             'status',
            # 'recieved_date',
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
            'status': forms.Select(attrs={
                'class': 'form-control',
                'id': 'status',
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
            # 'ordered_date': forms.DateTimeInput(attrs={
            #     'class': 'form-control',
            #     'id': 'order_date',
            #     'placeholder': 'Enter Date',
            #     'type': 'datetime-local',
            #     'name': 'order_date',
            # }),
            # 'recieved_date': forms.DateTimeInput(attrs={
            #     'class': 'form-control',
            #     'id': 'recieved_date',
            #     'placeholder': 'Enter Date',
            #     'type': 'datetime-local',
            #     'name': 'recieved_date',
            # }),
            # 'sub_department': forms.Select(attrs={
            #     'class': 'form-control',
            #     'id': 'sales_person',
            #     'placeholder': 'Name of the Vendor',
            #     'required': 'required',  # Make the field required
            # }),

        }


class WholesalePurchaseItemsForm(forms.ModelForm):
    class Meta:
        model = WholesalePurchaseItems
        fields = [
            'product',
            'quantity',
            'price',
            'discount_amount',
            'discount_value',
        ]
        widgets = {
            'product': forms.Select(attrs={
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

            'price': forms.TextInput(attrs={
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

# FormSet for multiple WholesalePurchaseItems entries
WholesalePurchaseItemsFormSet = forms.modelformset_factory(
    WholesalePurchaseItems,
    form=WholesalePurchaseItemsForm,
    extra=1,
)



# #--------------------------- Production --------------------------------#
# class WholesaleProductionForm(forms.ModelForm):
#     class Meta:
#         model = WholesaleProduction
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

# class WholesaleRawMaterialUsageForm(forms.ModelForm):
#     class Meta:
#         model = WholesaleRawMaterialUsage
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

# WholesaleRawMaterialUsageFormSet = modelformset_factory(WholesaleRawMaterialUsage, 
#                                                      form=WholesaleRawMaterialUsageForm, extra=1)
# #--------------------------- / Production --------------------------------#




# from .models import WholesaleInventory, WholesaleInventoryItems

# class WholesaleInventoryForm(forms.ModelForm):
#     class Meta:
#         model = WholesaleInventory
#         fields = ['employee', 'created']
#         widgets={
#             'employee':forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'status',
#                 'placeholder': 'Employee name',
#                 'required': 'required',  # Make the field required
#             }),
#             'created':forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'id': 'raw_material_product',
#                 'placeholder': 'Raw Material',
#                 'type': 'date',
#                 'required': 'required',  # Make the field required
#             }),
#         }

# class WholesaleInventoryItemsForm(forms.ModelForm):
#     class Meta:
#         model = WholesaleInventoryItems
#         fields = ['status', 'raw_material_name', 'quantity', 'price']
#         widgets={
#             'status':forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'status',
#                 'placeholder': 'status',
#                 'required': 'required',  # Make the field required
#             }),
#             'raw_material_name':forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'raw_material-product',
#                 'placeholder': 'Name of the Vendor',
#                 'required': 'required',  # Make the field required
#             }),
#             'quantity':forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'quantity',
#                 'placeholder': 'Quantity',
#                 'required': 'required',  # Make the field required
#                 "inputType": "number",
#                 "step": 1
#             }),
#             'price':forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'price',
#                 'placeholder': 'price',
#                 'required': 'required',
#                 # 'readonly':'readonly'  # Make the field required
#             }),
#         }



# WholesaleInventoryItemsFormSet = forms.modelformset_factory(
#     WholesaleInventoryItems,
#     form=WholesaleInventoryItemsForm,
#     extra=1,
# )



# from .models import WholesaleProductionOutput  # Replace with your actual model name

# class WholesaleProductionOutputForm(forms.ModelForm):
#     class Meta:
#         model = WholesaleProductionOutput  # Replace with your actual model name
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

# WholesaleProductionOutputFormset = forms.modelformset_factory(
#     WholesaleProductionOutput,
#     form=WholesaleProductionOutputForm,
#     extra=1,
# )