from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *

from django.utils.timezone import make_aware
from datetime import datetime

# Register your models here.
#############   #############   #############   #############   #############
#------------------------- Product / Category / Customer -----------------#
#############   #############   #############   #############   #############
class RawMaterialCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'raw_material_category_name']
    search_fields = []
    list_display_links = ['id', 'raw_material_category_name']

class RawMaterialsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'raw_material_name', 'category', 'tag', 'entry_measure', 'weight_pack', 'packaging', "raw_material_category" ]
    list_display_links = ['id', 'raw_material_name', 'category', 'entry_measure', 'weight_pack', "raw_material_category", "raw_material_category" ]
    list_per_page =500
    
    resource_class = RawMaterialsAdminResource
    
class BakeryProductAdmin(ImportExportModelAdmin):
    list_display = ['id', 'product_name', 'category', 'price', 'selling_price',
    "entry_weight_per_boule", 'weight_per_boule_kg', 'weight_per_boule_gram', 'output_per_boule',
    'unit_output_weight', 'recipe']
    search_fields = []
    list_display_links = ['id', 'product_name', ]

    resource_class = BakeryProductAdminResource

#=================================== Product Recipe ==================================#
class RecipeAdmin(ImportExportModelAdmin):
    list_display = ['id', 'recipe_name',]
    search_fields = []
    list_display_links = ['id', 'recipe_name',]
    
    resource_class = RecipeAdminResource

class ProductRecipeAdmin(ImportExportModelAdmin):
    list_display = ['id', 'product', 'recipe', 'quantity_per_product']
    search_fields = []
    list_display_links = ['id', 'product', 'recipe', 'quantity_per_product']

    resource_class = ProductRecipeAdminResource

class RecipeRawMaterialAdmin(ImportExportModelAdmin):
    list_display = ['id', 'recipe', 'raw_material', 'quantity_per_recipe', "measure"]
    search_fields = []
    list_display_links = ['id', 'recipe', 'raw_material', 'quantity_per_recipe', "measure"]
    
    resource_class = RecipeRawMaterialAdminResource 

#=================================== / Product Recipe ==================================#

class BakeryProductCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'category_name', 'sub_department']
    search_fields = []
    list_display_links = ['id', 'category_name', 'sub_department' ]
    resource_class = BakeryProductCategoryAdminResource

class BakeryCustomerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'customer_name', 'customer_type', 'area',
                    'company_name', 'phone', 'email',]
    search_fields = ['invoice_id__icontains', ]
    list_display_links = [ 'customer_name', 'customer_type',
                            'company_name', 'phone', 'email', ]

#############   #############   #############   #############   #############
    #------------------------- Invoicing --------------------------------#
#############   #############   #############   #############   #############

class BakeryCustomerOpeningBalanceAdmin(ImportExportModelAdmin):
    list_display = ['id', 'date', 'invoice', 'customer', 'description', 'amount_owed' ]
    search_fields = [ ]
    list_display_links = [ 'id', 'date', 'invoice', 'customer', 'description', 'amount_owed']
    list_per_page =500



class BakeryInvoiceAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'invoice_id','customer', 'sales_session',
                    'invoice_total', 'sales_person', 'due_date', 'vat_amount',]
    search_fields = [ ]
    list_display_links = ['id', 'created', 'customer',  ]
    list_per_page =500

    resource_class = BakeryInvoiceAdminResource
    

class BakeryInvoiceDetailAdmin(ImportExportModelAdmin):
    list_display = ['id',  'invoice', 'product', 'quantity', 'price',   'total',
    'discount_price', 'discount_value', 'net_amount' ]
    search_fields = [ ]
    list_display_links = ['id', 'invoice', 'product', 'quantity', 'price', 'total',
    'discount_price', 'discount_value', 'net_amount'  ]
    list_per_page =500
    resource_class = BakeryInvoiceDetailAdminResource

class BakeryInvoicePaymentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'date', 'customer', 'invoice_id',  'payment_installment', 'employee', 'amount_paid']
    search_fields = [ ]
    list_display_links = ['id', 'date', 'customer', 'invoice_id',  'payment_installment', 'employee', 'amount_paid']

    resource_class = BakeryInvoicePaymentAdminResource

#############   #############   #############   #############   #############
#------------------------- Bakery Supplier / Purchases ---------------------#
#############   #############   #############   #############   #############

class BakerySupplierAdmin(ImportExportModelAdmin):
    list_display = ['id', 'supplier_name', 'supplier_type', 'company_name', 'phone1', 'phone2', 'email',]
    search_fields = [ ]
    list_display_links = ['id', 'supplier_name', 'supplier_type','company_name', 'phone1', 'phone2', 'email',]


class BakeryPurchaseSummaryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'purchase_id', 'employee', 'supplier_name', 'description', 'purchase_value'
                    ,'amount_paid', 'balance_due', 'due_date']
    search_fields = [ ]
    list_display_links = ['id', 'created', 'purchase_id', 'employee', 'supplier_name', 'description', 'purchase_value'
                    ,'amount_paid', 'balance_due', 'due_date']
    
    resource_class = BakeryPurchaseSummaryAdminResource


class BakeryPurchaseAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created','supplier_name','purchase_id', 'employee',
                    'purchase_total', 'due_date', 'ordered_date', 'recieved_date']
    search_fields = [ ]
    list_display_links = ['id', 'created','supplier_name','purchase_id', 'employee', 
                    'purchase_total', 'due_date', 'ordered_date', 'recieved_date' ]

    resource_class = BakeryPurchaseAdminResource

class BakeryPurchaseItemsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'purchase_id', 'ordered_date', 'recieved_date', 'lead_time_days', 'raw_material',  'quantity', 'price', 'total', 
                    'discount_amount', 'discount_value', 'net_amount', "created",  "rm_total_qty_kg",]
    search_fields = [ ]
    list_display_links = ['id', 'purchase_id', 'ordered_date', 'lead_time_days', 'recieved_date', 'raw_material', 'quantity', 'price', 'total',  
                          'discount_amount', 'discount_value', 'net_amount', "created", "rm_total_qty_kg",]
    
    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     for item in queryset:
    #         if isinstance(item.purchase_date, datetime.date):
    #             # Convert to datetime with timezone awareness
    #             item.purchase_date = make_aware(datetime.combine(item.purchase_date, datetime.min.time()))
    #     return queryset

    resource_class = BakeryPurchaseItemsAdminResource


#############   #############   #############   #############   #############
    #------------------------- Bakery Inventory ---------------------#
#############   #############   #############   #############   #############

class BakeryInventoryAdmin(ImportExportModelAdmin):
    list_display = [ 'id', 'created', 'inventory_id', 'employee', 'department_name', 'total_cost' ]
    list_display_links = [ 'id', 'created', 'inventory_id', 'employee', 'department_name', 'total_cost' ]
    list_per_page =500

    resource_class = BakeryInventoryAdminResource

class BakeryInventoryItemsAdmin(ImportExportModelAdmin):
    list_display = [ 'id', 'created', 'inventory_id', 'status', 'raw_material_name', 
    'quantity', 'price', 'total', "rm_total_qty_kg", ]
    search_fields = [ ]
    list_display_links = [ 'id', 'created', 'inventory_id',  'status', 'raw_material_name', 
    'quantity', 'price', 'total', "rm_total_qty_kg", ]
    list_per_page = 500

    resource_class = BakeryInventoryItemsAdminResource
    

# Register your models here.
class BakeryProductionAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created_at', 'production_id', 'mixture_number', 'sub_department', 'session', 'supervisor', 'stock_supervisor'  ]
    list_display_links = ['id', 'created_at', 'production_id', 'mixture_number', 'sub_department', 'session', 'supervisor', 'stock_supervisor'  ]
    list_per_page =500

    resource_class = BakeryProductionAdminResource

class BakeryRawMaterialUsageAdmin(ImportExportModelAdmin):
    list_display = ['id',  'production_id', 'raw_material', 'qty', 'rm_total_weight_kg',
                    'unit_cost_price', 'raw_material_value', "avg_daily_demand", ]
    list_display_links = ['id', 'production_id',  'raw_material', 'qty', 'rm_total_weight_kg',
                    'unit_cost_price', 'raw_material_value' ]
    list_per_page =500

    resource_class = BakeryRawMaterialUsageAdminResource

class BakeryProductionOutputAdmin(ImportExportModelAdmin):
    list_display = ['id', 'production_id', 'mixture_number', 'output_category', 'tag', 'product', 'qty', 'product_price', 'value' ]
    list_display_links = ['id', 'production_id', 'mixture_number', 'product', 'output_category', 'tag', 'qty', 'product_price', 'value' ]
    list_per_page =500

    resource_class = BakeryProductionOutputAdminResource

class BakeryConsumptionDamagesAdmin(ImportExportModelAdmin):
    list_display = ['id', 'production_id', 'status', 'sub_department', 'session', 'employee', 'product', 'qty', 'product_price', 'value' ]
    list_display_links = ['id', 'production_id', 'status', 'sub_department', 'session', 'employee', 'product', 'qty', 'product_price', 'value']
    list_per_page =500

    resource_class = BakeryConsumptionDamagesAdminResource

class BakeryReturnsItemsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'date', 'customer', 'invoice', 'product', 'quantity', 'price', 'total', ]
    list_display_links = ['id', 'date', 'customer', 'invoice', 'product', 'quantity', 'price', 'total',]
    list_per_page =500

    #resource_class = BakeryConsumptionDamagesAdminResource
class BakeryProductUnitWeightAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'weight_per_boul', 'output_per_boul', 'product_unit_weight']
    list_display_links = ['id', 'product', 'weight_per_boul', 'output_per_boul', 'product_unit_weight']
    list_per_page = 500

    def save_model(self, request, obj, form, change):
        obj.product_unit_weight = obj.weight_per_boul / obj.output_per_boul
        super().save_model(request, obj, form, change)

admin.site.register(BakeryProductUnitWeight, BakeryProductUnitWeightAdmin)


# @admin.register(BakeryPurchasePayment)
# class BakeryPurchasePaymentAdmin(admin.ModelAdmin):
#     list_display = ['date', 'invoice', 'customer', 'payment_installment', 'amount_paid']]
#     list_filter = ['date', 'payment_installment']  # Optional: Add filters for better navigation
#     search_fields = ['invoice', 'customer']  # Optional: Add search fields for efficient searching


# admin.site.register(BakeryPurchasePayment, BakeryPurchasePaymentAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ProductRecipe, ProductRecipeAdmin)
admin.site.register(RecipeRawMaterial, RecipeRawMaterialAdmin)


admin.site.register(BakeryRawMaterialUsage, BakeryRawMaterialUsageAdmin)
admin.site.register(BakeryProduction, BakeryProductionAdmin)
admin.site.register(BakeryProductionOutput, BakeryProductionOutputAdmin)
admin.site.register(BakeryConsumptionDamages, BakeryConsumptionDamagesAdmin)
admin.site.register(BakeryCustomerOpeningBalance, BakeryCustomerOpeningBalanceAdmin)

admin.site.register(RawMaterialCategory, RawMaterialCategoryAdmin)
admin.site.register(RawMaterials, RawMaterialsAdmin)
admin.site.register(BakeryPurchase, BakeryPurchaseAdmin)
admin.site.register(BakeryPurchaseSummary, BakeryPurchaseSummaryAdmin)
admin.site.register(BakeryPurchaseItems, BakeryPurchaseItemsAdmin)
admin.site.register(BakerySupplier, BakerySupplierAdmin)

admin.site.register(BakeryInvoicePayment, BakeryInvoicePaymentAdmin)
admin.site.register(BakeryInvoice, BakeryInvoiceAdmin)
admin.site.register(BakeryInvoiceDetail, BakeryInvoiceDetailAdmin)

admin.site.register(BakeryCustomer, BakeryCustomerAdmin)
admin.site.register(BakeryProductCategory, BakeryProductCategoryAdmin)
admin.site.register(BakeryProduct, BakeryProductAdmin)

admin.site.register(BakeryInventory, BakeryInventoryAdmin)
admin.site.register(BakeryInventoryItems, BakeryInventoryItemsAdmin)

admin.site.register(BakeryReturnsItems, BakeryReturnsItemsAdmin)