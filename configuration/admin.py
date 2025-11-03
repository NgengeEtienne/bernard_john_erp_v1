from django.contrib import admin
from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *
# Register your models here.


class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ['id',  'department_name']
    search_fields = [ ]
    list_display_links = ['id',  'department_name']
    #list_per_page =30
    #list_filter = ('department','management_level','bank_name', 'accounts_dr', 'accounts_cr', )
    list_editable = ( )

class SubDepartmentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'department_name', 'sub_department_name']
    search_fields = [ ]
    list_display_links = ['id', 'department_name', 'sub_department_name']
    #list_per_page =30
    #list_filter = ('department','management_level','bank_name', 'accounts_dr', 'accounts_cr', )
    list_editable = ( )

    resource_class = SubDepatmentAdminResource

class SessionAdmin(ImportExportModelAdmin):
    list_display = ['id', 'session_name']
    search_fields = [ ]
    list_display_links = ['id', 'session_name']
    #list_per_page =30
    #list_filter = ('department','management_level','bank_name', 'accounts_dr', 'accounts_cr', )
    list_editable = ( )

class ManagementLevelAdmin(ImportExportModelAdmin):
    list_display = ['id', 'management_level']
    search_fields = [ ]
    list_display_links = ['id', 'management_level']
    #list_per_page =30
    #list_filter = ('department','management_level','bank_name', 'accounts_dr', 'accounts_cr', )
    list_editable = ( )

admin.site.register(Department,  DepartmentAdmin)
admin.site.register(SubDepartment,  SubDepartmentAdmin)
admin.site.register(Session,  SessionAdmin)
admin.site.register(ManagementLevel,  ManagementLevelAdmin)