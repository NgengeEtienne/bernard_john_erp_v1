from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *

# Register your models here.
#############   #############   #############   #############   #############
#------------------------- Product / Category -----------------#
#############   #############   #############   #############   #############

class BarProductAdmin(ImportExportModelAdmin):
    list_display = ['id', 'product_name', 'category', 'price', 'selling_price','unit_measure',]
    search_fields = []
    list_display_links = ['id', 'product_name', ]

    resource_class = BarProductAdminResource


class BarProductCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'category_name',]
    search_fields = []
    list_display_links = ['id', 'category_name', ]
    resource_class = BarProductCategoryAdminResource
    
class BarInventoryAdmin(ImportExportModelAdmin):
    list_display = [ 'id', 'created', 'inventory_id', 'employee',  'description', ]
    list_display_links = [ 'id', 'created', 'inventory_id', 'employee',  'description', ]
    list_per_page =500

    resource_class = BarInventoryAdminResource

class BarInventoryItemsAdmin(ImportExportModelAdmin):
    list_display = [ 'id', 'created', 'inventory_id',  'status', 'product_name', 'quantity', 
                    'cost_price', 'selling_price', 'total_cost_price', 'total_selling_price']
    search_fields = [ ]
    list_display_links = [ 'id', 'created', 'inventory_id',  'status', 'product_name', 'quantity', 'cost_price', 
                          'selling_price', 'total_cost_price', 'total_selling_price', ]
    list_per_page = 500

    resource_class = BarInventoryItemsAdminResource


class BarSupplierAdmin(ImportExportModelAdmin):
    list_display = ['id', 'supplier_name', 'supplier_type', 'company_name', 'phone1', 'phone2', 'email',]
    search_fields = [ ]
    list_display_links = ['id', 'supplier_name', 'supplier_type','company_name', 'phone1', 'phone2', 'email',]

class BarPurchaseSummaryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'purchase_id', 'employee', 'supplier_name', 'description', 'purchase_value'
                    ,'amount_paid', 'balance_due', 'due_date']
    search_fields = [ ]
    list_display_links = ['id', 'created', 'purchase_id', 'employee', 'supplier_name', 'description', 'purchase_value'
                    ,'amount_paid', 'balance_due', 'due_date']
    
    resource_class = BarPurchaseSummaryAdminResource

class BarPurchaseAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created','supplier_name','purchase_id', 'employee',
                    'purchase_total', 'due_date', 'vat_amount', 'discount_amount', 'net_amount']
    search_fields = [ ]
    list_display_links = ['id', 'created','supplier_name','purchase_id', 'employee',
                    'purchase_total', 'due_date', 'vat_amount', 'discount_amount', 'net_amount']

    resource_class = BarPurchaseAdminResource

class BarPurchaseItemsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'purchase_id', 'product_name',  'quantity', 'cost_price', 'total_cost_price', 
    'selling_price', 'total_selling_price', 'gross_profit']
    search_fields = [ ]
    list_display_links = ['id', 'purchase_id', 'product_name', 'quantity', 'cost_price', 'total_cost_price', 
    'selling_price', 'total_selling_price',  'gross_profit']

    resource_class = BarPurchaseItemsAdminResource
#------------------------- Product --------------------------------#
admin.site.register(BarProductCategory, BarProductCategoryAdmin)
admin.site.register(BarProduct, BarProductAdmin)

#------------------------- Inventory --------------------------------#
admin.site.register(BarInventory, BarInventoryAdmin)
admin.site.register(BarInventoryItems, BarInventoryItemsAdmin)


admin.site.register(BarSupplier, BarSupplierAdmin)
admin.site.register(BarPurchaseSummary, BarPurchaseSummaryAdmin)

admin.site.register(BarPurchase, BarPurchaseAdmin)
admin.site.register(BarPurchaseItems, BarPurchaseItemsAdmin)
