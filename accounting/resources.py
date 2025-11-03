from inspect import Attribute
from tkinter import Widget
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget,DateWidget
from .models import *


class AccountsSubCategoryAdminResource(resources.ModelResource):
    accounts_category = fields.Field(column_name='accounts_category', attribute='accounts_category',
                            widget=ForeignKeyWidget(AccountsCategory, field='account_category'))
    class Meta:
        model = AccountsSubCategory
        fields = ( 'id', 'account_sub_category', 'accounts_category' )
        

class AccountsDebitAdminResource(resources.ModelResource):
    accounts_sub_category = fields.Field(column_name='accounts_sub_category', attribute='accounts_sub_category',
                            widget=ForeignKeyWidget(AccountsSubCategory, field='account_sub_category'))
    class Meta:
        model = AccountsDebit
        fields = ( 'id', 'account_sub_category', 'account_debit' )
        
class AccountsCreditAdminResource(resources.ModelResource):
    accounts_sub_category = fields.Field(column_name='accounts_sub_category', attribute='accounts_sub_category',
                            widget=ForeignKeyWidget(AccountsSubCategory, field='account_sub_category'))
    class Meta:
        model = AccountsCredit
        fields = ( 'id', 'account_sub_category', 'account_credit')
        
        
class BakeryGeneralLedgerAdminResource(resources.ModelResource):
    accounts_debit = fields.Field(column_name='accounts_debit', attribute='accounts_debit',
                            widget=ForeignKeyWidget(AccountsDebit, field='account_debit'))
    
    accounts_credit = fields.Field(column_name='accounts_credit', attribute='accounts_credit',
                            widget=ForeignKeyWidget(AccountsCredit, field='account_credit'))
    
    department_name = fields.Field(column_name='department_name', attribute='department_name',
                            widget=ForeignKeyWidget(Department, field='department_name'))
    
    management_level = fields.Field(column_name='management_level', attribute='management_level',
                            widget=ForeignKeyWidget(ManagementLevel, field='management_level'))
    
    
    class Meta:
        model = BakeryGeneralLedger
        fields = ('id', 'created', 'department_name', 'management_level', 'employee_name', 'custom_user', 'institution',
                    'description', 'amount', 'accounts_debit', 'accounts_credit')
        
class SupermarketGeneralLedgerAdminResource(resources.ModelResource):
    accounts_debit = fields.Field(column_name='accounts_debit', attribute='accounts_debit',
                            widget=ForeignKeyWidget(AccountsDebit, field='account_debit'))
    
    accounts_credit = fields.Field(column_name='accounts_credit', attribute='accounts_credit',
                            widget=ForeignKeyWidget(AccountsCredit, field='account_credit'))
    
    department_name = fields.Field(column_name='department_name', attribute='department_name',
                            widget=ForeignKeyWidget(Department, field='department_name'))
    
    management_level = fields.Field(column_name='management_level', attribute='management_level',
                            widget=ForeignKeyWidget(ManagementLevel, field='management_level'))
    
    
    class Meta:
        model = SupermarketGeneralLedger
        fields = ('id', 'created', 'department_name', 'management_level', 'employee_name', 'custom_user', 'institution',
                    'description', 'amount', 'accounts_debit', 'accounts_credit')
        
class BoulangerieGeneralLedgerAdminResource(resources.ModelResource):
    accounts_debit = fields.Field(column_name='accounts_debit', attribute='accounts_debit',
                            widget=ForeignKeyWidget(AccountsDebit, field='account_debit'))
    
    accounts_credit = fields.Field(column_name='accounts_credit', attribute='accounts_credit',
                            widget=ForeignKeyWidget(AccountsCredit, field='account_credit'))
    
    department_name = fields.Field(column_name='department_name', attribute='department_name',
                            widget=ForeignKeyWidget(Department, field='department_name'))
    
    management_level = fields.Field(column_name='management_level', attribute='management_level',
                            widget=ForeignKeyWidget(ManagementLevel, field='management_level'))
    
    
    class Meta:
        model = BoulangerieGeneralLedger
        fields = ('id', 'created', 'department_name', 'management_level', 'employee_name', 'custom_user', 'institution',
                    'description', 'amount', 'accounts_debit', 'accounts_credit')
        
        
class BarGeneralLedgerAdminResource(resources.ModelResource):
    accounts_debit = fields.Field(column_name='accounts_debit', attribute='accounts_debit',
                            widget=ForeignKeyWidget(AccountsDebit, field='account_debit'))
    
    accounts_credit = fields.Field(column_name='accounts_credit', attribute='accounts_credit',
                            widget=ForeignKeyWidget(AccountsCredit, field='account_credit'))
    
    department_name = fields.Field(column_name='department_name', attribute='department_name',
                            widget=ForeignKeyWidget(Department, field='department_name'))
    
    management_level = fields.Field(column_name='management_level', attribute='management_level',
                            widget=ForeignKeyWidget(ManagementLevel, field='management_level'))
    
    
    class Meta:
        model = BarGeneralLedger
        fields = ('id', 'created', 'department_name', 'management_level', 'employee_name', 'custom_user', 'institution',
                    'description', 'amount', 'accounts_debit', 'accounts_credit')
        
        
        
class WholesaleGeneralLedgerAdminResource(resources.ModelResource):
    accounts_debit = fields.Field(column_name='accounts_debit', attribute='accounts_debit',
                            widget=ForeignKeyWidget(AccountsDebit, field='account_debit'))
    
    accounts_credit = fields.Field(column_name='accounts_credit', attribute='accounts_credit',
                            widget=ForeignKeyWidget(AccountsCredit, field='account_credit'))
    
    department_name = fields.Field(column_name='department_name', attribute='department_name',
                            widget=ForeignKeyWidget(Department, field='department_name'))
    
    management_level = fields.Field(column_name='management_level', attribute='management_level',
                            widget=ForeignKeyWidget(ManagementLevel, field='management_level'))
    
    class Meta:
        model = WholesaleGeneralLedger
        fields = ('id', 'created', 'department_name', 'management_level', 'employee_name', 'custom_user', 'institution',
                    'description', 'amount', 'accounts_debit', 'accounts_credit')