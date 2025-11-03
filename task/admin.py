from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['created', 'title', 'author',  'state', 'priority', 'expiry_date']
    #prepopulated_fields = {'slug': ('last_name',)} 'department', 'employee',

class EmployeeAdmin(ImportExportModelAdmin):
    list_display = ['id', 'employee',]

class AuthorAdmin(ImportExportModelAdmin):
    list_display = ['id', 'author',]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Employee, EmployeeAdmin)
