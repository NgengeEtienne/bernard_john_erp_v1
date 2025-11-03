from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin
from .resources import * 

# Register your models here.
class InvoicesAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created','supplier','invoice_id', 'sub_department', 'employee',
                    'invoice_total', 'due_date', 'vat_amount',]
    search_fields = [ ]
    list_display_links = ['id', 'created', 'employee', 'invoice_id', 'sub_department', 'supplier',  ]

    resource_class = InvoicesAdminResource

class InvoicesDetailAdmin(ImportExportModelAdmin):
    list_display = ['id',  'invoice', 'product', 'quantity', 'price',   'total',
    'discount_price', 'discount_value', 'net_amount' ]
    search_fields = [ ]
    list_display_links = ['id', 'invoice', 'product', 'quantity', 'price', 'total',
    'discount_price', 'discount_value', 'net_amount'  ]
    list_per_page =500
    resource_class = InvoicesDetailAdminResource

class PurchaseInvoicesPaymentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'date', 'supplier', 'invoice', 'payment_installment', 'employee',
                    'amount_paid', 'payment_id']
    search_fields = [ ]
    list_display_links = ['id', 'date',  'supplier', 'invoice', 'payment_installment', 'employee',  ]

    resource_class = PurchaseInvoicesPaymentAdminResource

#class ReturnsItemsAdmin(ImportExportModelAdmin):
    #list_display = ['id', 'sales_person', 'invoice', 'product','quantity', 'price',  'total', ]
    #search_fields = [ ]
    #list_display_links = ['id',  'sales_person', 'invoice','product','quantity', 'price',  'total',  ]

    #resource_class = PurchaseItemsAdminResource

admin.site.register(Invoices, InvoicesAdmin)
admin.site.register(InvoicesDetail, InvoicesDetailAdmin)
admin.site.register(PurchaseInvoicesPayment, PurchaseInvoicesPaymentAdmin)
#admin.site.register(ReturnsItems, ReturnsItemsAdmin)
