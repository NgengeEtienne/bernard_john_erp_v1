from inspect import Attribute
from tkinter import Widget
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget,DateWidget
from .models import *
from customer.models import *
from product.models import *


class InvoiceAdminResource(resources.ModelResource):
    customer = fields.Field(column_name='customer', attribute='customer',
                            widget=ForeignKeyWidget(Customer, field='customer_name'))
    class Meta:
        model = Invoice
        fields = ( 'id', 'created', 'invoice_id', 'customer', "sales_session" ,'due_date',  'message', 'invoice_total', )

class InvoiceDetailAdminResource(resources.ModelResource):
    invoice = fields.Field(column_name='invoice', attribute='invoice',
                        widget=ForeignKeyWidget(Invoice, field='invoice_id'))

    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(Product, field='product_name'))
    class Meta:
        model = InvoiceDetail
        fields = (
            'id', 'sales_person','invoice', 'product', 'quantity','price', 'amount',
            'discount_qty', 'discount_amount', 'total', 'discount_price', 'discount_value', 'net_amount' 
        )

class InvoicePaymentAdminResource(resources.ModelResource):
    invoice = fields.Field(column_name='invoice', attribute='invoice',
                            widget=ForeignKeyWidget(Invoice, field='invoice_id'))

    customer = fields.Field(column_name='customer', attribute='customer',
                            widget=ForeignKeyWidget(Customer, field='customer_name')) 
    class Meta:
        model = InvoicePayment
        fields = ( 'id', 'date', 'invoice', 'customer', "payment_session" ,'payment_installment',  'employee', 'amount_paid', )
-0

class ReturnsItemsAdminResource(resources.ModelResource):
    invoice = fields.Field(column_name='invoice', attribute='invoice',
                            widget=ForeignKeyWidget(Invoice, field='invoice_id'))

    customer = fields.Field(column_name='customer', attribute='customer',
                            widget=ForeignKeyWidget(Customer, field='customer_name'))

    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(Product, field='product_name'))
    class Meta:
        model = ReturnsItems
        fields = (
            'id', 'date', 'customer',  'invoice', 'product', 'quantity', 'price', 'total'
            )
'''
class PurchaseItemsAdminResource(resources.ModelResource):
    purchase_id = fields.Field(column_name='purchase_id', attribute='purchase_id',
                        widget=ForeignKeyWidget(Invoice, field='purchase_id'))

    raw_material_name= fields.Field(column_name='raw_material_name', attribute='raw_material_name',
                        widget=ForeignKeyWidget(RawMaterials, field='product'))
    class Meta:
        model = PurchaseItems
        fields = (
            'id', 'created','purchase_id', 'sub_department', 'status', 'raw_material_name', 'quantity', 'price', 'total',
            )
'''
