# bakery/forms.py
from django import forms
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django import forms
from django.forms import modelformset_factory

from .models import BakeryCustomer, BakeryProductCategory, BakeryProduction, BakeryRawMaterialUsage

class BakeryCustomerForm(forms.ModelForm):
    class Meta:
        model = BakeryCustomer
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

 

class BakeryProductCategoryForm(forms.ModelForm):
    class Meta:
        model = BakeryProductCategory
        fields = ['category_name', 'sub_department']  # Add fields you want in your form
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'sub_department': forms.Select(attrs={'class': 'form-control'}),
        }


from django import forms
from .models import BakeryInvoice, BakeryInvoiceDetail,BakeryConsumptionDamages

class BakeryInvoiceForm(forms.ModelForm):
    class Meta:
        model = BakeryInvoice
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
                'min': '0',  # Set the minimum value to 1
            }),
            'sales_person': forms.Select(attrs={
                'class': 'form-control',
                'id': 'sales_person',
                'placeholder': 'Name of the Vendor',
                'required': 'required',  # Make the field required
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',  # Bootstrap form-select and form-control classes
                'id': 'status',  # Keep the ID if necessary for JavaScript
                'placeholder': 'Select Tag...',
                'required': 'required',  # Make the field required
                'width':'150px',
            }),

        }


class BakeryInvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = BakeryInvoiceDetail
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
                'width':'150px',
            }),
 

            'quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_qty',
                'placeholder': '0',
                'type': 'number',
                'required': 'required',  # Make the field required
                'min': '0',  # Set the minimum value to 0
                'style': 'width: 150px;',
                "inputType": "number",
                
            }),

            'price': forms.TextInput(attrs={
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
            
 

            
        }


		
BakeryInvoiceDetailFormSet = formset_factory(BakeryInvoiceDetailForm, extra=1)


class BakeryConsumptionDamagesForm(forms.ModelForm):
    class Meta:
        model = BakeryConsumptionDamages
        fields = [
            'created_at',
            'session',
            'production_id',
            'employee',
             'status',
             'product',
             'qty',
             'product_price',
             'value',
             'sub_department'
        ]
  
        widgets = {

            'created_at': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'invoice_date',
                'placeholder': 'Enter date create',
                'type': 'date',
                'name': 'invoice_date',
            }),
 
            'session': forms.Select(attrs={
                'class': 'form-control',
                'id': 'session',
                'name': 'session',
                'placeholder': 'Select Session',
                'required': 'required',  # Make the field required
            }),
            'production_id': forms.Select(attrs={
                'class': 'form-control',
                'id': 'production_id',
                'name': 'production_id',
                'placeholder': 'Select production id',
                'required': 'required',  # Make the field required
            }),
           'sub_department': forms.Select(attrs={
                'class': 'form-control',
                'id': 'sub_department',
                'name': 'sub_department',
                'placeholder': 'Select Sub Department',
                'required': 'required',  # Make the field required
            }),
            'employee': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'sales_person',
                'placeholder': 'Name of the Vendor',
                'required': 'required',  # Make the field required
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',  # Bootstrap form-select and form-control classes
                'id': 'status',  # Keep the ID if necessary for JavaScript
                'placeholder': 'Select Tag...',
                'required': 'required',  # Make the field required
                'width':'150px',
            }),
            'product': forms.Select(attrs={
                'class': 'form-control',  # Bootstrap form-select and form-control classes
                'id': 'invoice_detail_product',  # Keep the ID if necessary for JavaScript
                'placeholder': 'Select product...',
                'required': 'required',  # Make the field required
                'width':'150px',
            }),
 

            'qty': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_qty',
                'placeholder': '0',
                'type': 'number',
                'required': 'required',  # Make the field required
                'min': '0',  # Set the minimum value to 0
                # 'style': 'width: 150px;',
                "inputType": "number",
                
            }),

            'product_price': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_price',
                'placeholder': '0',
                'type': 'number',
                'required': 'required',  # Make the field required
                'min': '0',
                'readonly':'readonly',
                'width':'50px',
            }),

            # 'value': forms.NumberInput(attrs={
            #     'class': 'form-control',
            #     'id': 'invoice_discount_price',
            #     'placeholder': '0',
            #     'type': 'number',
            #     'min': '0',
            #     'width':'50px',
            # }),

        }



from .models import BakeryPurchase, BakeryPurchaseItems

class BakeryPurchaseForm(forms.ModelForm):
    class Meta:
        model = BakeryPurchase
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
            'ordered_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'id': 'order_date',
                'placeholder': 'Enter Date',
                'type': 'datetime-local',
                'name': 'order_date',
            }),
            'recieved_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'id': 'recieved_date',
                'placeholder': 'Enter Date',
                'type': 'datetime-local',
                'name': 'recieved_date',
            }),
            'department': forms.Select(attrs={
                'class': 'form-control',
                'id': 'sales_person',
                'placeholder': 'Name of the Vendor',
                'required': 'required',  # Make the field required
            }),

        }


class BakeryPurchaseItemsForm(forms.ModelForm):
    class Meta:
        model = BakeryPurchaseItems
        fields = [
            'raw_material',
            'quantity',
            'price',
            'discount_amount',
            'discount_value',
        ]
        widgets = {
            'raw_material': forms.Select(attrs={
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
                'min': '0',  # Set the minimum value to 0
                'width':'60px',
                "inputType": "number",
                
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

# FormSet for multiple BakeryPurchaseItems entries
BakeryPurchaseItemsFormSet = forms.modelformset_factory(
    BakeryPurchaseItems,
    form=BakeryPurchaseItemsForm,
    extra=1,
)



#--------------------------- Production --------------------------------#
class BakeryProductionForm(forms.ModelForm):
    class Meta:
        model = BakeryProduction
        fields = [
            'created_at',
            'production_id',
            'department',
            'sub_department',
            'session',
            'supervisor',
            'stock_supervisor',
            'mixture_number',
        ]
  
        widgets = {
            'created_at': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'production_created_at',
                'placeholder': 'Enter Production Date',
                'type': 'date',
                'name': 'production_created_at',
            }),

            'department': forms.Select(attrs={
                'class': 'form-control',
                'id': 'production_department',
                'placeholder': 'Select Department',
                'required': 'required',
            }),
            'production_id': forms.Select(attrs={
                'class': 'form-control',
                'id': 'production_department',
                'placeholder': 'Select Department',
                'required': 'required',
            }),
 
            'sub_department': forms.Select(attrs={
                'class': 'form-control',
                'id': 'production_sub_department',
                'placeholder': 'Select Sub-Department',
                'required': 'required',
            }),

            'mixture_number': forms.Select(attrs={
                'class': 'form-control',
                'id': 'production_session',
                'placeholder': 'Select Session',
                'required': 'required',
            }),
            
            'session': forms.Select(attrs={
                'class': 'form-control',
                'id': 'production_session',
                'placeholder': 'Select Session',
                'required': 'required',
            }),

            'supervisor': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'production_supervisor',
                'placeholder': 'Name of the Supervisor',
                'required': 'required',
            }),
            
            'stock_supervisor': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'production_stock_supervisor',
                'placeholder': 'Name of the Stock Supervisor',
                'required': 'required',
            }),
            
            
        }

class BakeryRawMaterialUsageForm(forms.ModelForm):
    class Meta:
        model = BakeryRawMaterialUsage
        fields = [
            'raw_material',
            'status',
            'qty',
            'unit_cost_price'


        ]
        widgets = {
            
            
            'raw_material': forms.Select(attrs={
                'class': 'form-control ',
                'id': 'raw_material',
                'placeholder': 'Select Raw Material...',
                'required': 'required',
                'width':'60px',
            }),
              'status': forms.Select(attrs={
                'class': 'form-control ',
                'id': 'status',
                'placeholder': 'Select Raw Material...',
                'required': 'required',
                'width':'60px',
            }),
 
            'qty': forms.TextInput(attrs={
                'class': 'form-control ',
                'id': 'qty',
                'placeholder': '0',
                'type': 'number',
                'required': 'required',
                'min': '0',
                "inputType": "number",
                
                # 'style': 'width:300px;',
            }),
            
            'unit_cost_price': forms.TextInput(attrs={
                'class': 'form-control ',
                'id': 'qty',
                'placeholder': '0',
                'type': 'number',
                'required': 'required',
                'min': '0',
                'readonly':'readonly'
                #'style': 'width:300px;',
            }),
        }

BakeryRawMaterialUsageFormSet = modelformset_factory(BakeryRawMaterialUsage, 
                                                     form=BakeryRawMaterialUsageForm, extra=1)
#--------------------------- / Production --------------------------------#




from .models import BakeryInventory, BakeryInventoryItems

class BakeryInventoryForm(forms.ModelForm):
    class Meta:
        model = BakeryInventory
        fields = ['employee', 'created']
        widgets={
            'employee':forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'status',
                'placeholder': 'Employee name',
                'required': 'required',  # Make the field required
            }),
            'created':forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'raw_material_product',
                'placeholder': 'Raw Material',
                'type': 'date',
                'required': 'required',  # Make the field required
            }),
        }

class BakeryInventoryItemsForm(forms.ModelForm):
    class Meta:
        model = BakeryInventoryItems
        fields = ['status', 'raw_material_name', 'quantity', 'price']
        widgets={
            'status':forms.Select(attrs={
                'class': 'form-control',
                'id': 'status',
                'placeholder': 'status',
                'required': 'required',  # Make the field required
            }),
            'raw_material_name':forms.Select(attrs={
                'class': 'form-control',
                'id': 'raw_material-product',
                'placeholder': 'Name of the Vendor',
                'required': 'required',  # Make the field required
            }),
            'quantity':forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'quantity',
                'placeholder': 'Quantity',
                'required': 'required',  # Make the field required
                "inputType": "number",
                
            }),
            'price':forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'price',
                'placeholder': 'price',
                'required': 'required',
                 'readonly':'readonly'  # Make the field required
            }),
        }



BakeryInventoryItemsFormSet = forms.modelformset_factory(
    BakeryInventoryItems,
    form=BakeryInventoryItemsForm,
    extra=1,
)



from .models import BakeryProductionOutput  # Replace with your actual model name

class BakeryProductionOutputForm(forms.ModelForm):
    class Meta:
        model = BakeryProductionOutput  # Replace with your actual model name
        fields = [
           
            'output_category',
            'mixture_number',
            'tag',
            'product',
            'qty',
            'product_price',
            'value',
        ]
        widgets = {
    'output_category': forms.Select(attrs={
        'class': 'form-control ',
        'id': 'output_category',  # Adding id attribute
        'placeholder': 'Select Output Category',
        'required': 'required',
    }),
    'mixture_number': forms.Select(attrs={
        'class': 'form-control ',
        'id': 'mixture_number',  # Adding id attribute
        'placeholder': 'Select Mixture Number',
        'required': 'required',
    }),
    'tag': forms.Select(attrs={
        'class': 'form-control ',
        'id': 'tag',  # Adding id attribute
        'placeholder': 'Select Tag',
        'required': 'required',
    }),
    'product': forms.Select(attrs={
        'class': 'form-control ',
        'id': 'product',  # Adding id attribute
        'placeholder': 'Select Product',
        'required': 'required',
    }),
    'qty': forms.NumberInput(attrs={
        'class': 'form-control ',
        'id': 'qty',  # Adding id attribute
        'placeholder': 'Enter Quantity',
        "inputType": "number",
         'required': 'required',
    }),
    'product_price': forms.NumberInput(attrs={
        'class': 'form-control ',
        'id': 'product_price',  # Adding id attribute
        'placeholder': 'Enter Price',
        'readonly':'readonly',
        'required': 'required',
    }),
    'value': forms.NumberInput(attrs={
        'class': 'form-control ',
        'id': 'value',  # Adding id attribute
        'placeholder': 'Enter Output Value',
        # 'required': 'required',
    }),
}

BakeryProductionOutputFormset = forms.modelformset_factory(
    BakeryProductionOutput,
    form=BakeryProductionOutputForm,
    extra=1,
)

# views.py
# forms.py
from django import forms
from django.forms import modelformset_factory
from .models import RecipeRawMaterial

class RecipeRawMaterialForm(forms.ModelForm):
    class Meta:
        model = RecipeRawMaterial
        fields = ['id','recipe', 'raw_material', 'quantity_per_recipe', 'measure']
        id = forms.IntegerField(widget=forms.HiddenInput(), required=False)  # Add hidden ID field

        widgets = {
           'recipe': forms.Select(attrs={
               'name':'recipe',
                'class': 'form-control ',
                'id': 'recipe',  # Adding id attribute
                'placeholder': 'Select Recipe',
                'required': 'required',
            }),
            'raw_material': forms.Select(attrs={
                'class': 'form-control ',
                'id': 'product',  # Adding id attribute
                'placeholder': 'Select Raw Material',
                'required': 'required',
            }),
            'quantity_per_recipe': forms.NumberInput(attrs={
                'class': 'form-control ',
                'id': 'qty',  # Adding id attribute
                'placeholder': 'Enter Quantity in Grams',
                
                'required': 'required',
            }),
             'measure': forms.Select(attrs={
                'class': 'form-control ',
                'id': 'qty',  # Adding id attribute
                'placeholder': 'Enter Quantity',
                'required': 'required',
            }),
        }
# forms.py
RecipeRawMaterialFormSet = modelformset_factory(
    RecipeRawMaterial,
    form=RecipeRawMaterialForm,
    extra=1,  # Number of empty forms to display initially
    can_delete=True  # Allow deletion of forms
)


from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_name']
        widgets = {
            'recipe_name': forms.TextInput(attrs={'placeholder': 'Enter Recipe Name'}),
        }
