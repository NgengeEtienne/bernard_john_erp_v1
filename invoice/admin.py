from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *

# Register your models here.
class InvoiceAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'invoice_id','customer', 'sales_session',
                    'invoice_total', 'due_date', 'vat_amount',]
    search_fields = [ ]
    list_display_links = ['id', 'created', 'customer',  ]
    list_per_page =500

    resource_class = InvoiceAdminResource

class InvoiceDetailAdmin(ImportExportModelAdmin):
    list_display = ['id',  'sales_person', 'invoice', 'product', 'quantity', 'price',   'total',
    'discount_price', 'discount_value', 'net_amount' ]
    search_fields = [ ]
    list_display_links = ['id', 'sales_person', 'invoice', 'product', 'quantity', 'price', 'total',
    'discount_price', 'discount_value', 'net_amount'  ]
    list_per_page =500
    resource_class = InvoiceDetailAdminResource

class InvoicePaymentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'date', 'customer', 'invoice_id',  'payment_installment', 'employee', 'amount_paid']
    search_fields = [ ]
    list_display_links = ['id', 'date', 'customer', 'invoice_id',  'payment_installment', 'employee', 'amount_paid']

    resource_class = InvoicePaymentAdminResource



class ReturnsItemsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'date', 'customer', 'invoice', 'product','quantity', 'price',  'total', ]
    search_fields = [ ]
    list_display_links = ['id', 'date',  'customer', 'invoice','product','quantity', 'price',  'total',  ]

    resource_class = ReturnsItemsAdminResource

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceDetail, InvoiceDetailAdmin)
admin.site.register(InvoicePayment, InvoicePaymentAdmin)

admin.site.register(ReturnsItems, ReturnsItemsAdmin)
