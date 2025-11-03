from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class SupplierAdmin(ImportExportModelAdmin):
    list_display = ['id', 'supplier_name', 'supplier_type', 'company_name', 'phone1', 'phone2', 'email',]
    search_fields = [ ]
    list_display_links = ['id', 'supplier_name', 'supplier_type','company_name', 'phone1', 'phone2', 'email',]

admin.site.register(Supplier, SupplierAdmin)
