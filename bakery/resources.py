from inspect import Attribute
from tkinter import Widget
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget,DateWidget
from .models import *
from configuration.models import *


class RawMaterialsAdminResource(resources.ModelResource):
    raw_material_category = fields.Field(column_name='raw_material_category', attribute='raw_material_category',
                            widget=ForeignKeyWidget(RawMaterialCategory, field='raw_material_category_name'))
    class Meta:
        model = RawMaterials
        fields = ( 'id', 'raw_material_name', 'raw_material_category', "category", "perish_non_perish", 
                  "weight_pack", "entry_measure", "tag", "packaging", )

class BakeryProductCategoryAdminResource(resources.ModelResource):
    sub_department = fields.Field(column_name='sub_department', attribute='sub_department',
                            widget=ForeignKeyWidget(SubDepartment, field='sub_department_name'))
    class Meta:
        model = BakeryProductCategory
        fields = ( 'id', 'category_name', 'sub_department', )

class BakeryProductAdminResource(resources.ModelResource):
    category = fields.Field(column_name='category', attribute='category',
                        widget=ForeignKeyWidget(BakeryProductCategory, field='category_name'))

    recipe = fields.Field(column_name='recipe', attribute='recipe',
                        widget=ForeignKeyWidget(Recipe, field='recipe_name'))
    
    class Meta:
        model = BakeryProduct
        fields = (
            'id','created','product_name', 'category', 'price', 'selling_price', 'slug',
            "entry_weight_per_boule", 'weight_per_boule_kg', 'weight_per_boule_gram', 'output_per_boule',
    'unit_output_weight', 'recipe',
        )

#############   #############   #############   #############   #############
    #------------------------- Invoicing --------------------------------#
#############   #############   #############   #############   #############

class BakeryInvoiceAdminResource(resources.ModelResource):
    customer = fields.Field(column_name='customer', attribute='customer',
                            widget=ForeignKeyWidget(BakeryCustomer, field='customer_name'))
    class Meta:
        model = BakeryInvoice
        fields = ( 'id', 'created', 'invoice_id', 'customer', "sales_session" ,'due_date',  'message', 'invoice_total', )

class BakeryInvoiceDetailAdminResource(resources.ModelResource):
    invoice = fields.Field(column_name='invoice', attribute='invoice',
                        widget=ForeignKeyWidget(BakeryInvoice, field='invoice_id'))

    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(BakeryProduct, field='product_name'))
    class Meta:
        model = BakeryInvoiceDetail
        fields = (
            'id', 'sales_person','invoice', 'product', 'quantity','price', 'amount',
            'discount_qty', 'discount_amount', 'total', 'discount_price', 'discount_value', 'net_amount' 
        )

class BakeryInvoicePaymentAdminResource(resources.ModelResource):
    invoice = fields.Field(column_name='invoice', attribute='invoice',
                        widget=ForeignKeyWidget(BakeryInvoice, field='invoice_id'))

    customer = fields.Field(column_name='customer', attribute='customer',
                            widget=ForeignKeyWidget(BakeryCustomer, field='customer_name')) 
    class Meta:
        model = BakeryInvoicePayment
        fields = ( 'id', 'date', 'invoice', 'customer', "payment_session" ,'payment_installment',  'employee', 'amount_paid', )

#############   #############   #############   #############   #############
    #------------------------- Purchases Invoicing --------------------------------#
#############   #############   #############   #############   #############
class BakeryPurchaseSummaryAdminResource(resources.ModelResource):
    supplier_name = fields.Field(column_name='supplier_name', attribute='supplier_name',
                            widget=ForeignKeyWidget(BakerySupplier, field='supplier_name'))
    class Meta:
        model = BakeryPurchaseSummary
        fields = ( 'id', 'created', 'purchase_id', 'employee', 'supplier_name', 'description', 'purchase_value'
                    ,'amount_paid', 'balance_due', 'due_date' )
        

class BakeryPurchaseAdminResource(resources.ModelResource):
    supplier_name = fields.Field(column_name='supplier_name', attribute='supplier_name',
                            widget=ForeignKeyWidget(BakerySupplier, field='supplier_name'))
    class Meta:
        model = BakeryPurchase
        fields = ( 'id', 'created','supplier_name','purchase_id', 'employee',
                    'purchase_total', 'due_date', 'vat_amount', 'ordered_date', 'recieved_date' , 
                    'discount_amount', 'net_amount', 'lead_time_days',)


class BakeryPurchaseItemsAdminResource(resources.ModelResource):
    purchase_id = fields.Field(column_name='purchase_id', attribute='purchase_id',
                        widget=ForeignKeyWidget(BakeryPurchase, field='purchase_id'))

    raw_material= fields.Field(column_name='raw_material', attribute='raw_material',
                        widget=ForeignKeyWidget(RawMaterials, field='raw_material_name'))
    class Meta:
        model = BakeryPurchaseItems
        fields = (
            'id', 'purchase_id', 'raw_material_name',  'quantity', 'price', 'total', "created", 
            "rm_total_qty_kg", 'ordered_date', 'recieved_date', 'lead_time_days',
            )


#############   #############   #############   #############   #############
    #------------------------- Inventory --------------------------------#
#############   #############   #############   #############   #############
class BakeryInventoryAdminResource(resources.ModelResource):
    department_name = fields.Field(column_name='department_name', attribute='department_name',
                        widget=ForeignKeyWidget(Department, field='department_name'))


    class Meta:
        model = BakeryInventory
        fields = (
            'id', 'created', 'inventory_id', 'employee', 'department_name',
        )

class BakeryInventoryItemsAdminResource(resources.ModelResource):
    inventory_id = fields.Field(column_name='inventory_id', attribute='inventory_id',
                        widget=ForeignKeyWidget(BakeryInventory, field='inventory_id'))

    #sub_department = fields.Field(column_name='sub_department', attribute='sub_department',
                        #widget=ForeignKeyWidget(Department, field='department_name'))

    raw_material_name = fields.Field(column_name='raw_material_name', attribute='raw_material_name',
                        widget=ForeignKeyWidget(RawMaterials, field='raw_material_name'))
    class Meta:
        model = BakeryInventoryItems
        fields = (
            'id', 'created', 'inventory_id', 'employee', 'status', 'raw_material_name', 
            'quantity', 'price', 'total', "rm_total_qty_kg",
        )

#############   #############   #############   #############   #############
    #------------------------- Production --------------------------------#
#############   #############   #############   #############   #############
class BakeryProductionAdminResource(resources.ModelResource):
    sub_department = fields.Field(column_name='sub_department', attribute='sub_department',
                        widget=ForeignKeyWidget(SubDepartment, field='sub_department_name'))

    class Meta:
        model = BakeryProduction
        fields = (
            'id', 'created_at', 'production_id', 'mixture_number', 'department', 'sub_department', 
            'session', 'supervisor', 'stock_supervisor',
                    )

class BakeryRawMaterialUsageAdminResource(resources.ModelResource):
    production_id = fields.Field(column_name='production_id', attribute='production_id',
                        widget=ForeignKeyWidget(BakeryProduction, field='production_id'))

    raw_material = fields.Field(column_name='raw_material', attribute='raw_material',
                        widget=ForeignKeyWidget(RawMaterials, field='raw_material_name'))

    class Meta:
        model = BakeryRawMaterialUsage
        fields = (
            'id',  'production_id',  'raw_material', 'qty', 'rm_total_weight_grams',
            'unit_cost_price', 'raw_material_value', "avg_daily_demand",
        )

#--------------------------------------------------------------------------------------------------------#

class BakeryProductionOutputAdminResource(resources.ModelResource):
    production_id = fields.Field(column_name='production_id', attribute='production_id',
                        widget=ForeignKeyWidget(BakeryProduction, field='production_id'))

    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(BakeryProduct, field='product_name'))

    class Meta:
        model = BakeryProductionOutput
        fields = (
            'id', 'production_id','mixture_number', 'output_category', 'tag', 'product', 'qty', 'product_price', 'value'
        )

class BakeryConsumptionDamagesAdminResource(resources.ModelResource):
    production_id = fields.Field(column_name='production_id', attribute='production_id',
                        widget=ForeignKeyWidget(BakeryProduction, field='production_id'))

    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(BakeryProduct, field='product_name'))

    sub_department = fields.Field(column_name='sub_department', attribute='sub_department',
                        widget=ForeignKeyWidget(SubDepartment, field='department_name'))

    class Meta:
        model = BakeryConsumptionDamages
        fields = (
            'id', 'production_id', 'status', 'sub_department', 'session', 'product', 'qty', 'product_price', 'value' 
        )

#=================================== Product Recipe ==================================#
class RecipeAdminResource(resources.ModelResource):

    class Meta:
        model = Recipe
        fields = (
            'id', 'recipe_name',
        )
        
class ProductRecipeAdminResource(resources.ModelResource):
    recipe = fields.Field(column_name='recipe', attribute='recipe',
                        widget=ForeignKeyWidget(Recipe, field='recipe_name'))
    
    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(BakeryProduct, field='product_name'))
    class Meta:
        model = ProductRecipe
        fields = (
            'id', 'product', 'recipe', 'quantity_per_product',
        )
        
class RecipeRawMaterialAdminResource(resources.ModelResource):
    recipe = fields.Field(column_name='recipe', attribute='recipe',
                        widget=ForeignKeyWidget(Recipe, field='recipe_name'))
    
    raw_material = fields.Field(column_name='raw_material', attribute='raw_material',
                        widget=ForeignKeyWidget(RawMaterials, field='raw_material_name'))
    
    class Meta:
        model = RecipeRawMaterial
        fields = (
            'id', 'recipe', 'raw_material', 'quantity_per_recipe', 'measure'
        )