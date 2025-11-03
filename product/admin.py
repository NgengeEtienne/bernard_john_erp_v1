from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *
# Register your models here.
class ProductAdmin(ImportExportModelAdmin):
    list_display = ['id', 'product_name', 'category', 'price', 'selling_price',
    "entry_weight_per_boule", 'weight_per_boule_kg', 'weight_per_boule_gram', 'output_per_boule',
    'unit_output_weight',]
    search_fields = []
    list_display_links = ['id', 'product_name', ]

    resource_class = ProductAdminResource


class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'category_name', 'department' ]
    search_fields = []
    list_display_links = ['id', 'category_name', ]
    resource_class = CategoryAdminResource


class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'department_name', ]
    search_fields = []
    list_display_links = ['id', 'department_name', ]

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
