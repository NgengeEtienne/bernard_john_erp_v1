from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *

# Register your models here.
class SupermarketProductSubCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'sub_category_name',]
    search_fields = []
    list_display_links = ['id', 'sub_category_name', ]
    
    resource_class = SupermarketProductSubCategoryAdminResource
    
  
class SupermarketProductAdmin(ImportExportModelAdmin):
    list_display = ['id', 'product_name', 'sub_category_name', 'barcode', 'cost_price', 'selling_price', ]
    search_fields = []
    list_per_page = 300
    list_display_links = ['id', 'product_name', 'sub_category_name', 'barcode', 'cost_price', 'selling_price',]
    
    resource_class = SupermarketProductAdminResource
    
    
class SupermarketCustomerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'customer_name', 'customer_type', 'area',
                    'company_name', 'phone', 'email',]
    search_fields = ['invoice_id__icontains', ]
    list_display_links = [ 'customer_name', 'customer_type',
                            'company_name', 'phone', 'email', ]


class SupermarketInvoiceAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'department_name', 'invoice_id','customer', 'sales_session',
                    'invoice_total', 'due_date', 'vat_amount',]
    search_fields = [ ]
    list_display_links = ['id', 'created', 'customer',  ]
    list_per_page =500

    resource_class = SupermarketInvoiceAdminResource
    

class SupermarketInvoiceDetailAdmin(ImportExportModelAdmin):
    list_display = ['id', 'invoice', 'product', 'quantity', 'price',
                    'total', 'discount_price', 'discount_value', 'net_amount' ]
    search_fields = [ ]
    list_display_links = ['id',  'invoice', 'product', 'quantity', 'price', 
                    'total','discount_price', 'discount_value', 'net_amount' ]
    list_per_page =500
    
    resource_class = SupermarketInvoiceDetailAdminResource


#############   #############   #############   #############   #############
#------------------------- Supermarket Supplier / Purchases ----------------#
#############   #############   #############   #############   #############

class SupermarketSupplierAdmin(ImportExportModelAdmin):
    list_display = ['id', 'supplier_name', 'supplier_type', 'company_name', 'phone1', 'phone2', 'email',]
    search_fields = [ ]
    list_display_links = ['id', 'supplier_name', 'supplier_type','company_name', 'phone1', 'phone2', 'email',]


class SupermarketPurchaseSummaryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'purchase_id', 'employee', 'supplier_name', 'description', 'purchase_value'
                    ,'amount_paid', 'balance_due', 'due_date']
    search_fields = [ ]
    list_display_links = ['id', 'created', 'purchase_id', 'employee', 'supplier_name', 'description', 'purchase_value'
                    ,'amount_paid', 'balance_due', 'due_date']
    
    resource_class = SupermarketPurchaseSummaryAdminResource
    

class SupermarketPurchaseAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created','supplier_name','purchase_id', 'employee', "department",
                    'purchase_total', 'due_date', 'vat_amount', 'discount_amount', 'net_amount']
    search_fields = [ ]
    list_display_links = ['id', 'created','supplier_name','purchase_id', 'employee',
                    'purchase_total', 'due_date', 'vat_amount', 'discount_amount', 'net_amount']

    resource_class = SupermarketPurchaseAdminResource

class SupermarketPurchaseItemsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'purchase_id', 'product',  'quantity', 'unit_selling_price', 'total_selling_price', "net_amount"]
    search_fields = [ ]
    list_display_links = ['id', 'purchase_id', 'product', 'quantity', 'unit_selling_price', 'total_selling_price', ]

    resource_class = SupermarketPurchaseItemsAdminResource



admin.site.register(SupermarketPurchase, SupermarketPurchaseAdmin)
admin.site.register(SupermarketPurchaseSummary, SupermarketPurchaseSummaryAdmin)
admin.site.register(SupermarketPurchaseItems, SupermarketPurchaseItemsAdmin)
admin.site.register(SupermarketSupplier, SupermarketSupplierAdmin)

admin.site.register(SupermarketInvoice, SupermarketInvoiceAdmin)
admin.site.register(SupermarketInvoiceDetail, SupermarketInvoiceDetailAdmin)
admin.site.register(SupermarketProductSubCategory, SupermarketProductSubCategoryAdmin)
admin.site.register(SupermarketProduct, SupermarketProductAdmin)
admin.site.register(SupermarketCustomer, SupermarketCustomerAdmin)