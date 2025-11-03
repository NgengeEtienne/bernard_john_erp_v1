from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'customer_name', 'customer_type', 'area',
                    'company_name', 'phone', 'email',]
    search_fields = ['invoice_id__icontains', ]
    list_display_links = [ 'customer_name', 'customer_type',
                            'company_name', 'phone', 'email', ]

admin.site.register(Customer, CustomerAdmin)
