from inspect import Attribute
from tkinter import Widget
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget,DateWidget
from .models import *

        
class WholesaleProductSubCategoryAdminResource(resources.ModelResource):
    class Meta:
        model = WholesaleProductSubCategory
        fields = ( 'id','sub_category_name', )

class WholesaleProductAdminResource(resources.ModelResource):
    sub_category_name = fields.Field(column_name='sub_category_name', attribute='sub_category_name',
                            widget=ForeignKeyWidget(WholesaleProductSubCategory, field='sub_category_name'))
    class Meta:
        model = WholesaleProduct
        fields = ( 'id', 'product_name', 'sub_category_name', 'barcode', 'cost_price', 'selling_price', 'reorder_level' )


class WholesaleInvoiceAdminResource(resources.ModelResource):
    department_name = fields.Field(column_name='department_name', attribute='department_name',
                            widget=ForeignKeyWidget(Department, field='department_name'))
    customer = fields.Field(column_name='customer', attribute='customer',
                            widget=ForeignKeyWidget(WholesaleCustomer, field='customer_name'))
    class Meta:
        model = WholesaleInvoice
        fields = ( 'id', 'created', 'department_name', 'invoice_id',  'customer', "sales_session" ,'due_date',  'message', 'invoice_total', )


class WholesaleInvoiceDetailAdminResource(resources.ModelResource):
    invoice = fields.Field(column_name='invoice', attribute='invoice',
                        widget=ForeignKeyWidget(WholesaleInvoice, field='invoice_id'))

    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(WholesaleProduct, field='product_name'))
    class Meta:
        model = WholesaleInvoiceDetail
        fields = (
            'id', 'sales_person', 'invoice', 'delivery_man', 'product', 'quantity', 'unit_cost_price', 'unit_selling_price',
                    'total_cost_price', 'total_selling_price', 'discount_price', 'discount_value', 'net_amount' 
        )

class WholesaleInvoicePaymentAdminResource(resources.ModelResource):
    invoice = fields.Field(column_name='invoice', attribute='invoice',
                        widget=ForeignKeyWidget(WholesaleInvoice, field='invoice_id'))

    customer = fields.Field(column_name='customer', attribute='customer',
                            widget=ForeignKeyWidget(WholesaleCustomer, field='customer_name')) 
    class Meta:
        model = WholesaleInvoicePayment
        fields = ( 'id', 'date', 'invoice', 'customer', "payment_session" ,'payment_installment',  'employee', 'amount_paid', )


class WholesaleOpeningBalanceAdminResource(resources.ModelResource):
    invoice = fields.Field(column_name='invoice', attribute='invoice',
                        widget=ForeignKeyWidget(WholesaleInvoice, field='invoice_id'))

    customer = fields.Field(column_name='customer', attribute='customer',
                            widget=ForeignKeyWidget(WholesaleCustomer, field='customer_name'))
    
    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(WholesaleProduct, field='product_name'))
    class Meta:
        model = WholesaleOpeningBalance
        fields = ( 'id', 'date', 'invoice', 'customer', 'product', 'quantity', 'price', 'total', )


#############   #############   #############   #############   #############
    #------------------------- Purchases Invoicing --------------------------------#
#############   #############   #############   #############   #############
class WholesalePurchaseSummaryAdminResource(resources.ModelResource):
    supplier_name = fields.Field(column_name='supplier_name', attribute='supplier_name',
                            widget=ForeignKeyWidget(WholesaleSupplier, field='supplier_name'))
    class Meta:
        model = WholesalePurchaseSummary
        fields = ( 'id', 'created', 'purchase_id', 'employee', 'supplier_name', 'description', 'purchase_value'
                    ,'amount_paid', 'balance_due', 'due_date' )
        

class WholesalePurchaseAdminResource(resources.ModelResource):
    supplier_name = fields.Field(column_name='supplier_name', attribute='supplier_name',
                            widget=ForeignKeyWidget(WholesaleSupplier, field='supplier_name'))
    class Meta:
        model = WholesalePurchase
        fields = ( 'id', 'created', 'employee','supplier_name','purchase_id', 'purchase_total', 
                  'due_date', 'vat_amount', 'discount_amount', 'net_amount')


class WholesalePurchaseItemsAdminResource(resources.ModelResource):
    purchase_id = fields.Field(column_name='purchase_id', attribute='purchase_id',
                        widget=ForeignKeyWidget(WholesalePurchase, field='purchase_id'))

    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(WholesaleProduct, field='product_name'))
    class Meta:
        model = WholesalePurchaseItems
        fields = (
            'id', 'purchase_id', 'product',  'quantity', 'price', 'total',
            )
        
'''

#############   #############   #############   #############   #############
    #------------------------- Inventory --------------------------------#
#############   #############   #############   #############   #############
class WholesaleInventoryAdminResource(resources.ModelResource):
    department_name = fields.Field(column_name='department_name', attribute='department_name',
                        widget=ForeignKeyWidget(Department, field='department_name'))


    class Meta:
        model = WholesaleInventory
        fields = (
            'id', 'created', 'inventory_id', 'employee', 'department_name',
        )

class WholesaleInventoryItemsAdminResource(resources.ModelResource):
    inventory_id = fields.Field(column_name='inventory_id', attribute='inventory_id',
                        widget=ForeignKeyWidget(WholesaleInventory, field='inventory_id'))

    #sub_department = fields.Field(column_name='sub_department', attribute='sub_department',
                        #widget=ForeignKeyWidget(Department, field='department_name'))

    raw_material_name = fields.Field(column_name='raw_material_name', attribute='raw_material_name',
                        widget=ForeignKeyWidget(RawMaterials, field='raw_material_name'))
    class Meta:
        model = WholesaleInventoryItems
        fields = (
            'id', 'created', 'inventory_id', 'employee', 'status', 'raw_material_name', 'quantity', 'price', 'total',
        )

'''