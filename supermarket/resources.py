from inspect import Attribute
from tkinter import Widget
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget,DateWidget
from .models import *

        
class SupermarketProductSubCategoryAdminResource(resources.ModelResource):
    class Meta:
        model = SupermarketProductSubCategory
        fields = ( 'id','sub_category_name', )

class SupermarketProductAdminResource(resources.ModelResource):
    sub_category_name = fields.Field(column_name='sub_category_name', attribute='sub_category_name',
                            widget=ForeignKeyWidget(SupermarketProductSubCategory, field='sub_category_name'))
    class Meta:
        model = SupermarketProduct
        fields = ( 'id', 'product_name', 'sub_category_name', 'barcode', 'cost_price', 'selling_price', )


class SupermarketInvoiceAdminResource(resources.ModelResource):
    department_name = fields.Field(column_name='department_name', attribute='department_name',
                            widget=ForeignKeyWidget(Department, field='department_name'))
    customer = fields.Field(column_name='customer', attribute='customer',
                            widget=ForeignKeyWidget(SupermarketCustomer, field='customer_name'))
    class Meta:
        model = SupermarketInvoice
        fields = ( 'id', 'created', 'department_name', 'invoice_id', 'customer', "sales_session" ,'due_date',  'message', 'invoice_total', )


class SupermarketInvoiceDetailAdminResource(resources.ModelResource):
    invoice = fields.Field(column_name='invoice', attribute='invoice',
                        widget=ForeignKeyWidget(SupermarketInvoice, field='invoice_id'))

    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(SupermarketProduct, field='product_name'))
    class Meta:
        model = SupermarketInvoiceDetail
        fields = (
            'id', 'sales_person', 'invoice', 'product', 'quantity', 'unit_cost_price', 'unit_selling_price',
                    'total_cost_price', 'total_selling_price', 'discount_price', 'discount_value', 'net_amount' 
        )





#############   #############   #############   #############   #############
    #------------------------- Purchases Invoicing --------------------------------#
#############   #############   #############   #############   #############
class SupermarketPurchaseSummaryAdminResource(resources.ModelResource):
    supplier_name = fields.Field(column_name='supplier_name', attribute='supplier_name',
                            widget=ForeignKeyWidget(SupermarketSupplier, field='supplier_name'))
    class Meta:
        model = SupermarketPurchaseSummary
        fields = ( 'id', 'created', 'purchase_id', 'employee', 'supplier_name', 'description', 'purchase_value'
                    ,'amount_paid', 'balance_due', 'due_date' )
        

class SupermarketPurchaseAdminResource(resources.ModelResource):
    supplier_name = fields.Field(column_name='supplier_name', attribute='supplier_name',
                            widget=ForeignKeyWidget(SupermarketSupplier, field='supplier_name'))
    
    department = fields.Field(column_name='department', attribute='department',
                            widget=ForeignKeyWidget(Department, field='department_name'))
    class Meta:
        model = SupermarketPurchase
        fields = ( 'id', 'created', "ordered_date", "recieved_date", 'department', 'employee','supplier_name','purchase_id', 'purchase_total', 
                  'due_date', 'vat_amount', 'discount_amount', 'net_amount')


class SupermarketPurchaseItemsAdminResource(resources.ModelResource):
    purchase_id = fields.Field(column_name='purchase_id', attribute='purchase_id',
                        widget=ForeignKeyWidget(SupermarketPurchase, field='purchase_id'))

    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(SupermarketProduct, field='product_name'))
    class Meta:
        model = SupermarketPurchaseItems
        fields = (
            'id', 'created', "ordered_date", "recieved_date", 'purchase_id', 'product',  
            'quantity', 'unit_cost_price', 'unit_cost_price','unit_selling_price',
            'discount_price','discount_value',
            )
        
'''

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
            'id', 'created', 'inventory_id', 'employee', 'status', 'raw_material_name', 'quantity', 'price', 'total',
        )

'''