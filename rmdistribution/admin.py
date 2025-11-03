from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin
#from .resources import *

# Register your models here.


class RmDistributionAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'distribution_id', 'employee', 'sub_department',   ]
    list_display_links = ['id', 'created', 'distribution_id', 'employee',   ]
    list_per_page =500

    #resource_class = InventoryAdminResource

class RmDistributionItemsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'distribution_id', 'status',  'raw_material', 'quantity', 'price', 'total', ]
    search_fields = [ ]
    list_display_links = ['id', 'created', 'distribution_id', 'status', 'raw_material', 'quantity', 'price', 'total', ]
    list_per_page = 500

    #resource_class = InventoryItemsAdminResource



admin.site.register(RmDistribution, RmDistributionAdmin)
admin.site.register(RmDistributionItems, RmDistributionItemsAdmin)
