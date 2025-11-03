from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *

# Register your models here.
class WholesaleProductSubCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'sub_category_name',]
    search_fields = []
    list_display_links = ['id', 'sub_category_name', ]
    
    resource_class = WholesaleProductSubCategoryAdminResource
    
  
class WholesaleProductAdmin(ImportExportModelAdmin):
    list_display = ['id', 'product_name', 'sub_category_name', 'barcode', 'cost_price', 'selling_price', 'reorder_level', ]
    search_fields = []
    list_display_links = ['id', 'product_name', 'sub_category_name', 'barcode', 'cost_price', 'selling_price', 'reorder_level',]
    
    resource_class = WholesaleProductAdminResource
    
    
class WholesaleCustomerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'customer_name', 'customer_type', 'area',
                    'company_name', 'phone', 'email',]
    search_fields = ['invoice_id__icontains', ]
    list_display_links = [ 'customer_name', 'customer_type',
                            'company_name', 'phone', 'email', ]


class WholesaleInvoiceAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created',  'invoice_id','customer', 'status',
                    'invoice_total', 'due_date', ]
    search_fields = [ ]
    list_display_links = ['id', 'created', 'customer',  ]
    list_per_page =500

    resource_class = WholesaleInvoiceAdminResource
    

class WholesaleInvoiceDetailAdmin(ImportExportModelAdmin):
    list_display = ['id', 'sales_person', 'invoice', 'delivery_man', 'product', 'quantity', 'unit_cost_price', 'unit_selling_price',
                    'total_cost_price', 'total_selling_price', 'discount_price', 'discount_value', 'net_amount' ]
    search_fields = [ ]
    list_display_links = ['id', 'sales_person', 'invoice', 'delivery_man', 'product', 'quantity', 'unit_cost_price', 'unit_selling_price',
                    'total_cost_price', 'total_selling_price', 'discount_price', 'discount_value', 'net_amount' ]
    list_per_page =500
    
    resource_class = WholesaleInvoiceDetailAdminResource

class WholesaleInvoicePaymentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'date', 'customer', 'invoice_id',  'payment_installment', 'employee', 'amount_paid']
    search_fields = [ ]
    list_display_links = ['id', 'date', 'customer', 'invoice_id',  'payment_installment', 'employee', 'amount_paid']

    resource_class = WholesaleInvoicePaymentAdminResource

class WholesaleOpeningBalanceAdmin(ImportExportModelAdmin):
    list_display = ['id', 'date', 'customer', 'invoice', 'product', 'quantity', 'price', 'total', ]
    list_display_links = ['id', 'date', 'customer', 'invoice', 'product', 'quantity', 'price', 'total',]
    list_per_page =500

    resource_class = WholesaleOpeningBalanceAdminResource
    
#############   #############   #############   #############   #############
#------------------------- Wholesale Supplier / Purchases ----------------#
#############   #############   #############   #############   #############

class WholesaleSupplierAdmin(ImportExportModelAdmin):
    list_display = ['id', 'supplier_name', 'supplier_type', 'company_name', 'phone1', 'phone2', 'email',]
    search_fields = [ ]
    list_display_links = ['id', 'supplier_name', 'supplier_type','company_name', 'phone1', 'phone2', 'email',]


class WholesalePurchaseSummaryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'purchase_id', 'employee', 'supplier_name', 'description', 'purchase_value'
                    ,'amount_paid', 'balance_due', 'due_date']
    search_fields = [ ]
    list_display_links = ['id', 'created', 'purchase_id', 'employee', 'supplier_name', 'description', 'purchase_value'
                    ,'amount_paid', 'balance_due', 'due_date']
    
    resource_class = WholesalePurchaseSummaryAdminResource
    

class WholesalePurchaseAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created','supplier_name','purchase_id', 'employee',
                    'purchase_total', 'due_date',  'net_amount']
    search_fields = [ ]
    list_display_links = ['id', 'created','supplier_name','purchase_id', 'employee',
                    'purchase_total', 'due_date',  'net_amount']

    resource_class = WholesalePurchaseAdminResource

class WholesalePurchaseItemsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'purchase_id', 'product',  'quantity', 'price', 'discount_amount', 'discount_value','total', ]
    search_fields = [ ]
    list_display_links = ['id', 'purchase_id', 'product', 'quantity', 'price', 'discount_amount', 'discount_value', 'total', ]

    resource_class = WholesalePurchaseItemsAdminResource

admin.site.register(WholesaleOpeningBalance, WholesaleOpeningBalanceAdmin)
admin.site.register(WholesaleInvoicePayment, WholesaleInvoicePaymentAdmin)

admin.site.register(WholesalePurchase, WholesalePurchaseAdmin)
admin.site.register(WholesalePurchaseSummary, WholesalePurchaseSummaryAdmin)
admin.site.register(WholesalePurchaseItems, WholesalePurchaseItemsAdmin)
admin.site.register(WholesaleSupplier, WholesaleSupplierAdmin)

admin.site.register(WholesaleInvoice, WholesaleInvoiceAdmin)
admin.site.register(WholesaleInvoiceDetail, WholesaleInvoiceDetailAdmin)
admin.site.register(WholesaleProductSubCategory, WholesaleProductSubCategoryAdmin)
admin.site.register(WholesaleProduct, WholesaleProductAdmin)
admin.site.register(WholesaleCustomer, WholesaleCustomerAdmin)