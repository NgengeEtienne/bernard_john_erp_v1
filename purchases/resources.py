
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget,DateWidget
from .models import *
from supplier.models import *
from product.models import *


class InvoicesAdminResource(resources.ModelResource):
    supplier = fields.Field(column_name='supplier', attribute='supplier',
                            widget=ForeignKeyWidget(Supplier, field='supplier_name'))
    class Meta:
        model = Invoices
        fields = ( 'id', 'created', 'invoice_id', 'supplier', "employee" , 'sub_department', 'due_date',  'invoice_total', 'vat_amount' )


class InvoicesDetailAdminResource(resources.ModelResource):
    invoice = fields.Field(column_name='invoice', attribute='invoice',
                        widget=ForeignKeyWidget(Invoices, field='invoice_id'))

    product= fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(RawMaterials, field='product'))
    class Meta:
        model = InvoicesDetail
        fields = (
            'id', 'invoice', 'sub_department', 'status', 'product', 'quantity', 'price', 'total',
            )


class PurchaseInvoicesPaymentAdminResource(resources.ModelResource):
    invoice = fields.Field(column_name='invoice', attribute='invoice',
                        widget=ForeignKeyWidget(Invoices, field='invoice_id'))

    supplier = fields.Field(column_name='supplier', attribute='supplier',
                            widget=ForeignKeyWidget(Supplier, field='supplier_name'))
    class Meta:
        model = PurchaseInvoicesPayment
        fields = (
            'id', 'date', 'invoice', 'support', 'supplier', 'employee', 'amount_paid', 'payment_id',
            )
