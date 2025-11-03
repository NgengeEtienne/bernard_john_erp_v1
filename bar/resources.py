from inspect import Attribute
from tkinter import Widget
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget,DateWidget
from .models import *


class BarProductCategoryAdminResource(resources.ModelResource):
    #sub_department = fields.Field(column_name='sub_department', attribute='sub_department',
                            #widget=ForeignKeyWidget(SubDepartment, field='sub_department_name'))
    class Meta:
        model = BarProductCategory
        fields = ( 'id', 'category_name',)

class BarProductAdminResource(resources.ModelResource):
    category = fields.Field(column_name='category', attribute='category',
                        widget=ForeignKeyWidget(BarProductCategory, field='category_name'))
    class Meta:
        model = BarProduct
        fields = (
            'id','created','product_name', 'category', 'price', 'selling_price', 'slug', "unit_measure",
        )

#############   #############   #############   #############   #############
    #------------------------- Inventory --------------------------------#
#############   #############   #############   #############   #############
class BarInventoryAdminResource(resources.ModelResource):
    department_name = fields.Field(column_name='department_name', attribute='department_name',
                        widget=ForeignKeyWidget(Department, field='department_name'))


    class Meta:
        model = BarInventory
        fields = (
            'id', 'created', 'inventory_id', 'employee', 'department_name','description',
        )

class BarInventoryItemsAdminResource(resources.ModelResource):
    inventory_id = fields.Field(column_name='inventory_id', attribute='inventory_id',
                        widget=ForeignKeyWidget(BarInventory, field='inventory_id'))

    #sub_department = fields.Field(column_name='sub_department', attribute='sub_department',
                        #widget=ForeignKeyWidget(Department, field='department_name'))

    product_name = fields.Field(column_name='product_name', attribute='product_name',
                        widget=ForeignKeyWidget(BarProduct, field='product_name'))
    class Meta:
        model = BarInventoryItems
        fields = (
            'id', 'created', 'inventory_id', 'employee', 'status', 'product_name', 'quantity', 'cost_price', 'selling_price', 'total_cost_price', 'total_selling_price'
        )


#############   #############   #############   #############   #############
    #------------------------- Purchases Invoicing --------------------------------#
#############   #############   #############   #############   #############
class BarPurchaseSummaryAdminResource(resources.ModelResource):
    supplier_name = fields.Field(column_name='supplier_name', attribute='supplier_name',
                            widget=ForeignKeyWidget(BarSupplier, field='supplier_name'))
    class Meta:
        model = BarPurchaseSummary
        fields = ( 'id', 'created', 'purchase_id', 'employee', 'supplier_name', 'description', 'purchase_value'
                    ,'amount_paid', 'balance_due', 'due_date' )
        

class BarPurchaseAdminResource(resources.ModelResource):
    supplier_name = fields.Field(column_name='supplier_name', attribute='supplier_name',
                            widget=ForeignKeyWidget(BarSupplier, field='supplier_name'))
    class Meta:
        model = BarPurchase
        fields = ( 'id', 'created','supplier_name','purchase_id', 'employee',
                    'purchase_total', 'due_date', 'vat_amount', 'discount_amount', 'net_amount')


class BarPurchaseItemsAdminResource(resources.ModelResource):
    purchase_id = fields.Field(column_name='purchase_id', attribute='purchase_id',
                        widget=ForeignKeyWidget(BarPurchase, field='purchase_id'))

    product_name= fields.Field(column_name='product_name', attribute='product_name',
                        widget=ForeignKeyWidget(BarProduct, field='product_name'))
    class Meta:
        model = BarPurchaseItems
        fields = (
            'id', 'purchase_id', 'product_name', 'quantity', 'cost_price', 'total_cost_price', 
            'selling_price', 'total_selling_price',  'gross_profit'
            )
