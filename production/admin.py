from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *

# Register your models here.
class ProductionAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created_at', 'production_id', 'sub_department', 'session', 'supervisor',  ]
    list_display_links = ['id', 'created_at', 'production_id', 'sub_department', 'session', 'supervisor',  ]
    list_per_page =500

    resource_class = ProductionAdminResource

class RawMaterialUsageAdmin(ImportExportModelAdmin):
    list_display = ['id',  'production_id', 'mixture_number',  'raw_material', 'qty', 'rm_total_weight_grams',
                    'unit_cost_price', 'raw_material_value' ]
    list_display_links = ['id', 'mixture_number', 'production_id',  'raw_material', 'qty', 'rm_total_weight_grams',
                    'unit_cost_price', 'raw_material_value' ]
    list_per_page =500

    resource_class = RawMaterialUsageAdminResource

class ProductionOutputAdmin(ImportExportModelAdmin):
    list_display = ['id', 'production_id', 'mixture_number', 'output_category', 'product', 'qty', 'product_price', 'value' ]
    list_display_links = ['id', 'production_id', 'mixture_number', 'product', 'output_category', 'qty', 'product_price', 'value' ]
    list_per_page =500

    resource_class = ProductionOutputAdminResource

class ConsumptionDamagesAdmin(ImportExportModelAdmin):
    list_display = ['id', 'production_id', 'status', 'product', 'qty', 'product_price', 'value' ]
    list_display_links = ['id', 'production_id', 'status', 'product', 'qty', 'product_price', 'value' ]
    list_per_page =500

    resource_class = ConsumptionDamagesAdminResource


admin.site.register(RawMaterialUsage, RawMaterialUsageAdmin)
admin.site.register(Production, ProductionAdmin)
admin.site.register(ProductionOutput, ProductionOutputAdmin)
admin.site.register(ConsumptionDamages, ConsumptionDamagesAdmin)
