from inspect import Attribute
from tkinter import Widget
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget,DateWidget
from .models import *

        
class BoulangerieProductSubCategoryAdminResource(resources.ModelResource):
    class Meta:
        model = BoulangerieProductSubCategory
        fields = ( 'id','sub_category_name', )

class BoulangerieProductAdminResource(resources.ModelResource):
    sub_category_name = fields.Field(column_name='sub_category_name', attribute='sub_category_name',
                            widget=ForeignKeyWidget(BoulangerieProductSubCategory, field='sub_category_name'))
    class Meta:
        model = BoulangerieProduct
        fields = ( 'id', 'product_name', 'sub_category_name', 'barcode', 'cost_price', 'selling_price', 'reorder_level' )


class BoulangerieInvoiceAdminResource(resources.ModelResource):
    department_name = fields.Field(column_name='department_name', attribute='department_name',
                            widget=ForeignKeyWidget(Department, field='department_name'))
    customer = fields.Field(column_name='customer', attribute='customer',
                            widget=ForeignKeyWidget(BoulangerieCustomer, field='customer_name'))
    class Meta:
        model = BoulangerieInvoice
        fields = ( 'id', 'created', 'department_name', 'invoice_id',  'customer', "sales_session" ,'due_date',  'message', 'invoice_total', )


class BoulangerieInvoiceDetailAdminResource(resources.ModelResource):
    invoice = fields.Field(column_name='invoice', attribute='invoice',
                        widget=ForeignKeyWidget(BoulangerieInvoice, field='invoice_id'))

    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(BoulangerieProduct, field='product_name'))
    class Meta:
        model = BoulangerieInvoiceDetail
        fields = (
            'id', 'sales_person', 'invoice', 'delivery_man', 'product', 'quantity', 'unit_cost_price', 'unit_selling_price',
                    'total_cost_price', 'total_selling_price', 'discount_price', 'discount_value', 'net_amount' 
        )

class BoulangerieInvoicePaymentAdminResource(resources.ModelResource):
    invoice = fields.Field(column_name='invoice', attribute='invoice',
                        widget=ForeignKeyWidget(BoulangerieInvoice, field='invoice_id'))

    customer = fields.Field(column_name='customer', attribute='customer',
                            widget=ForeignKeyWidget(BoulangerieCustomer, field='customer_name')) 
    class Meta:
        model = BoulangerieInvoicePayment
        fields = ( 'id', 'date', 'invoice', 'customer', "payment_session" ,'payment_installment',  'employee', 'amount_paid', )


class BoulangerieOpeningBalanceAdminResource(resources.ModelResource):
    invoice = fields.Field(column_name='invoice', attribute='invoice',
                        widget=ForeignKeyWidget(BoulangerieInvoice, field='invoice_id'))

    customer = fields.Field(column_name='customer', attribute='customer',
                            widget=ForeignKeyWidget(BoulangerieCustomer, field='customer_name'))
    
    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(BoulangerieProduct, field='product_name'))
    class Meta:
        model = BoulangerieOpeningBalance
        fields = ( 'id', 'date', 'invoice', 'customer', 'product', 'quantity', 'price', 'total', )


#############   #############   #############   #############   #############
    #------------------------- Purchases Invoicing --------------------------------#
#############   #############   #############   #############   #############
class BoulangeriePurchaseSummaryAdminResource(resources.ModelResource):
    supplier_name = fields.Field(column_name='supplier_name', attribute='supplier_name',
                            widget=ForeignKeyWidget(BoulangerieSupplier, field='supplier_name'))
    class Meta:
        model = BoulangeriePurchaseSummary
        fields = ( 'id', 'created', 'purchase_id', 'employee', 'supplier_name', 'description', 'purchase_value'
                    ,'amount_paid', 'balance_due', 'due_date' )
        

class BoulangeriePurchaseAdminResource(resources.ModelResource):
    supplier_name = fields.Field(column_name='supplier_name', attribute='supplier_name',
                            widget=ForeignKeyWidget(BoulangerieSupplier, field='supplier_name'))
    class Meta:
        model = BoulangeriePurchase
        fields = ( 'id', 'created', 'employee','supplier_name','purchase_id', 'purchase_total', 
                  'due_date', 'vat_amount', 'discount_amount', 'net_amount')


class BoulangeriePurchaseItemsAdminResource(resources.ModelResource):
    purchase_id = fields.Field(column_name='purchase_id', attribute='purchase_id',
                        widget=ForeignKeyWidget(BoulangeriePurchase, field='purchase_id'))

    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(BoulangerieProduct, field='product_name'))
    class Meta:
        model = BoulangeriePurchaseItems
        fields = (
            'id', 'purchase_id', 'product',  'quantity', 'price', 'total',
            )
        
'''

#############   #############   #############   #############   #############
    #------------------------- Inventory --------------------------------#
#############   #############   #############   #############   #############
class BoulangerieInventoryAdminResource(resources.ModelResource):
    department_name = fields.Field(column_name='department_name', attribute='department_name',
                        widget=ForeignKeyWidget(Department, field='department_name'))


    class Meta:
        model = BoulangerieInventory
        fields = (
            'id', 'created', 'inventory_id', 'employee', 'department_name',
        )

class BoulangerieInventoryItemsAdminResource(resources.ModelResource):
    inventory_id = fields.Field(column_name='inventory_id', attribute='inventory_id',
                        widget=ForeignKeyWidget(BoulangerieInventory, field='inventory_id'))

    #sub_department = fields.Field(column_name='sub_department', attribute='sub_department',
                        #widget=ForeignKeyWidget(Department, field='department_name'))

    raw_material_name = fields.Field(column_name='raw_material_name', attribute='raw_material_name',
                        widget=ForeignKeyWidget(RawMaterials, field='raw_material_name'))
    class Meta:
        model = BoulangerieInventoryItems
        fields = (
            'id', 'created', 'inventory_id', 'employee', 'status', 'raw_material_name', 'quantity', 'price', 'total',
        )

'''