from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *


class AccountsCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'account_category', ]
    search_fields = [ ]
    list_display_links = ['id', 'account_category', ]
    list_per_page =500
    
class AccountsSubCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'account_sub_category', 'accounts_category' ]
    search_fields = [ ]
    list_display_links = ['id', 'account_sub_category', 'accounts_category' ]
    list_per_page =500
    
    resource_class = AccountsSubCategoryAdminResource
    
class AccountsDebitAdmin(ImportExportModelAdmin):
    list_display = ['id', 'accounts_sub_category', 'account_debit', ]
    search_fields = [ ]
    list_display_links = ['id', 'accounts_sub_category', 'account_debit', ]
    list_per_page =500
    
    resource_class = AccountsDebitAdminResource
    
class AccountsCreditAdmin(ImportExportModelAdmin):
    list_display = ['id', 'accounts_sub_category', 'account_credit', ]
    search_fields = [ ]
    list_display_links = ['id', 'accounts_sub_category', 'account_credit', ]
    list_per_page =500
    
    resource_class = AccountsCreditAdminResource
    
class BakeryGeneralLedgerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'department_name', 'management_level', 'employee_name', 
                    'custom_user', 'institution', 'description', 'amount', 'accounts_debit', 'accounts_credit']
    search_fields = [ ]
    list_display_links = ['id', 'created', 'department_name', 'management_level', 'employee_name',
                          'custom_user', 'institution','description', 'amount', 'accounts_debit', 'accounts_credit']
    list_per_page =500

    resource_class = BakeryGeneralLedgerAdminResource


class SupermarketGeneralLedgerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'department_name', 'management_level', 'employee_name', 
                    'custom_user', 'institution', 'description', 'amount', 'accounts_debit', 'accounts_credit']
    search_fields = [ ]
    list_display_links = ['id', 'created', 'department_name', 'management_level', 'employee_name',
                          'custom_user', 'institution','description', 'amount', 'accounts_debit', 'accounts_credit']
    list_per_page =500
    
    resource_class = SupermarketGeneralLedgerAdminResource
    
class BoulangerieGeneralLedgerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'department_name', 'management_level', 'employee_name', 
                    'custom_user', 'institution', 'description', 'amount', 'accounts_debit', 'accounts_credit']
    search_fields = [ ]
    list_display_links = ['id', 'created', 'department_name', 'management_level', 'employee_name',
                          'custom_user', 'institution','description', 'amount', 'accounts_debit', 'accounts_credit']
    list_per_page =500
    
    resource_class = BoulangerieGeneralLedgerAdminResource
    
class BarGeneralLedgerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'department_name', 'management_level', 'employee_name', 
                    'custom_user', 'institution', 'description', 'amount', 'accounts_debit', 'accounts_credit']
    search_fields = [ ]
    list_display_links = ['id', 'created', 'department_name', 'management_level', 'employee_name',
                          'custom_user', 'institution','description', 'amount', 'accounts_debit', 'accounts_credit']
    list_per_page =500
    
    resource_class = BarGeneralLedgerAdminResource
    
class WholesaleGeneralLedgerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created', 'department_name', 'management_level', 'employee_name', 
                    'custom_user', 'institution', 'description', 'amount', 'accounts_debit', 'accounts_credit']
    search_fields = [ ]
    list_display_links = ['id', 'created', 'department_name', 'management_level', 'employee_name',
                          'custom_user', 'institution','description', 'amount', 'accounts_debit', 'accounts_credit']
    list_per_page =500
    
    resource_class = WholesaleGeneralLedgerAdminResource


admin.site.register(WholesaleGeneralLedger, WholesaleGeneralLedgerAdmin)

admin.site.register(AccountsCategory, AccountsCategoryAdmin)
admin.site.register(AccountsSubCategory, AccountsSubCategoryAdmin)
admin.site.register(AccountsDebit, AccountsDebitAdmin)
admin.site.register(AccountsCredit, AccountsCreditAdmin)

admin.site.register(BakeryGeneralLedger, BakeryGeneralLedgerAdmin)
admin.site.register(SupermarketGeneralLedger, SupermarketGeneralLedgerAdmin)
admin.site.register(BarGeneralLedger, BarGeneralLedgerAdmin)
admin.site.register(BoulangerieGeneralLedger, BoulangerieGeneralLedgerAdmin)