from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *

# Register your models here.
class BoulangerieProductSubCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'sub_category_name',]
    search_fields = []
    list_display_links = ['id', 'sub_category_name', ]
    
    resource_class = BoulangerieProductSubCategoryAdminResource
    
  
class BoulangerieProductAdmin(ImportExportModelAdmin):
    list_display = ['id', 'product_name', 'sub_category_name', 'barcode', 'cost_price', 'selling_price', 'reorder_level', ]
    search_fields = []
    list_display_links = ['id', 'product_name', 'sub_category_name', 'barcode', 'cost_price', 'selling_price', 'reorder_level',]
    
    resource_class = BoulangerieProductAdminResource
    
    
class BoulangerieCustomerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'customer_name', 'customer_type', 'area',
                    'company_name', 'phone', 'email',]
    search_fields = ['invoice_id__icontains', ]
    list_display_links = [ 'customer_name', 'customer_type',
                            'company_name', 'phone', 'email', ]


class BoulangerieInvoiceAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created',  'invoice_id','customer', 'status',
                    'invoice_total', 'due_date', ]
    search_fields = [ ]
    list_display_links = ['id', 'created', 'customer',  ]
    list_per_page =500

    resource_class = BoulangerieInvoiceAdminResource
    

class BoulangerieInvoiceDetailAdmin(ImportExportModelAdmin):
    list_display = ['id', 'sales_person', 'invoice', 'delivery_man', 'product', 'quantity', 'unit_cost_price', 'unit_selling_price',
                    'total_cost_price', 'total_selling_price', 'discount_price', 'discount_value', 'net_amount' ]
    search_fields = [ ]
    list_display_links = ['id', 'sales_person', 'invoice', 'delivery_man', 'product', 'quantity', 'unit_cost_price', 'unit_selling_price',
                    'total_cost_price', 'total_selling_price', 'discount_price', 'discount_value', 'net_amount' ]
    list_per_page =500
    
    resource_class = BoulangerieInvoiceDetailAdminResource

class BoulangerieInvoicePaymentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'date', 'customer', 'invoice_id',  'payment_installment', 'employee', 'amount_paid']
    search_fields = [ ]
    list_display_links = ['id', 'date', 'customer', 'invoice_id',  'payment_installment', 'employee', 'amount_paid']

    resource_class = BoulangerieInvoicePaymentAdminResource

class BoulangerieOpeningBalanceAdmin(ImportExportModelAdmin):
    list_display = ['id', 'date', 'customer', 'invoice', 'product', 'quantity', 'price', 'total', ]
    list_display_links = ['id', 'date', 'customer', 'invoice', 'product', 'quantity', 'price', 'total',]
    list_per_page =500

    resource_class = BoulangerieOpeningBalanceAdminResource
    
#############   #############   #############   #############   #############
#------------------------- Boulangerie Supplier / Purchases ----------------#
#############   #############   #############   #############   #############

class BoulangerieSupplierAdmin(ImportExportModelAdmin):
    list_display = ['id', 'supplier_name', 'supplier_type', 'company_name', 'phone1', 'phone2', 'email',]
    search_fields = [ ]
    list_display_links = ['id', 'supplier_name', 'supplier_type','company_name', 'phone1', 'phone2', 'email',]


class BoulangeriePurchaseSummaryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'purchase_id', 'employee', 'supplier_name', 'description', 'purchase_value'
                    ,'amount_paid', 'balance_due', 'due_date']
    search_fields = [ ]
    list_display_links = ['id', 'created', 'purchase_id', 'employee', 'supplier_name', 'description', 'purchase_value'
                    ,'amount_paid', 'balance_due', 'due_date']
    
    resource_class = BoulangeriePurchaseSummaryAdminResource
    

class BoulangeriePurchaseAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created','supplier_name','purchase_id', 'employee',
                    'purchase_total', 'due_date',  'net_amount']
    search_fields = [ ]
    list_display_links = ['id', 'created','supplier_name','purchase_id', 'employee',
                    'purchase_total', 'due_date',  'net_amount']

    resource_class = BoulangeriePurchaseAdminResource

class BoulangeriePurchaseItemsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'purchase_id', 'product',  'quantity', 'price', 'discount_amount', 'discount_value','total', ]
    search_fields = [ ]
    list_display_links = ['id', 'purchase_id', 'product', 'quantity', 'price', 'discount_amount', 'discount_value', 'total', ]

    resource_class = BoulangeriePurchaseItemsAdminResource

admin.site.register(BoulangerieOpeningBalance, BoulangerieOpeningBalanceAdmin)
admin.site.register(BoulangerieInvoicePayment, BoulangerieInvoicePaymentAdmin)

admin.site.register(BoulangeriePurchase, BoulangeriePurchaseAdmin)
admin.site.register(BoulangeriePurchaseSummary, BoulangeriePurchaseSummaryAdmin)
admin.site.register(BoulangeriePurchaseItems, BoulangeriePurchaseItemsAdmin)
admin.site.register(BoulangerieSupplier, BoulangerieSupplierAdmin)

admin.site.register(BoulangerieInvoice, BoulangerieInvoiceAdmin)
admin.site.register(BoulangerieInvoiceDetail, BoulangerieInvoiceDetailAdmin)
admin.site.register(BoulangerieProductSubCategory, BoulangerieProductSubCategoryAdmin)
admin.site.register(BoulangerieProduct, BoulangerieProductAdmin)
admin.site.register(BoulangerieCustomer, BoulangerieCustomerAdmin)