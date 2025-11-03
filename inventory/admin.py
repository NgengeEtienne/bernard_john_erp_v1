from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *

# Register your models here.
class RawMaterialsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'product', 'category', 'entry_measure', 'weight_pack', 'packaging' ]
    list_display_links = ['id', 'product', 'category', 'entry_measure', 'weight_pack', ]
    list_per_page =500

class InventoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'inventory_id', 'employee', 'sub_department',   ]
    list_display_links = ['id', 'created', 'inventory_id', 'employee',   ]
    list_per_page =500

    resource_class = InventoryAdminResource

class InventoryItemsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'inventory_id', 'employee', 'status',  'raw_material', 'quantity', 'price', 'total', ]
    search_fields = [ ]
    list_display_links = ['id', 'inventory_id', 'employee', 'status', 'raw_material', 'quantity', 'price', 'total', ]
    list_per_page = 500

    resource_class = InventoryItemsAdminResource






admin.site.register(RawMaterials, RawMaterialsAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(InventoryItems, InventoryItemsAdmin)
