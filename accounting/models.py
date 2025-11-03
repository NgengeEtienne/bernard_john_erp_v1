from django.db import models

# Create your models here.
from django.db import models
from django.template.defaultfilters import slugify
import datetime
from decimal import Decimal
from django.urls import reverse
from django.utils.timezone import now
from configuration.models import *
from django.core.validators import RegexValidator, MinValueValidator
import uuid
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Sum
from configuration.models import Department



#############   #############   #############   #############   #############
#------------------------- Chart of Accounts  ------------------------------#
#############   #############   #############   #############   #############

class AccountsCategory(models.Model):
    
    account_category =  models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name = 'Accounts Debit')

    def __str__(self):
        return self.account_category

    class Meta():
        verbose_name = 'Accounts Category'
        verbose_name_plural = 'Accounts Categories'
        #ordering: ['-created_at']

class AccountsSubCategory(models.Model):
    accounts_category =  models.ForeignKey(AccountsCategory, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Accounts Category')
    account_sub_category =  models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name = 'Accounts Sub Category')

    def __str__(self):
        return self.account_sub_category

    class Meta():
        verbose_name = 'Accounts Sub Category'
        verbose_name_plural = 'Accounts Sub Categories'
        #ordering: ['-created_at']

class AccountsDebit(models.Model):
    accounts_sub_category =  models.ForeignKey(AccountsSubCategory, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Accounts Sub Category')
    account_debit =  models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name = 'Accounts Debit')

    def __str__(self):
        return self.account_debit

    class Meta():
        verbose_name = 'Accounts Debit'
        verbose_name_plural = 'Accounts Debit'
        #ordering: ['-created_at']

class AccountsCredit(models.Model):
    accounts_sub_category =  models.ForeignKey(AccountsSubCategory, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Accounts Sub Category')
    account_credit =  models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name = 'Accounts Credit')

    def __str__(self):
        return self.account_credit

    class Meta():
        verbose_name = 'Accounts Credit'
        verbose_name_plural = 'Accounts Credit'
        #ordering: ['-created_at']

#############   #############   #############   #############   #############
#------------------------- Bakery General Ledger  ------------------------------#
#############   #############   #############   #############   #############

class BakeryGeneralLedger(models.Model):
    created = models.DateField(default=now, verbose_name = "Date")
    department_name =  models.ForeignKey(Department, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Department')
    management_level = models.ForeignKey(ManagementLevel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Management Level",
                                         help_text='Management or Employee')
    employee_name = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="Employee Name", 
                                     help_text='Name of Employee Performing the Transaction')
    custom_user = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="User", 
                                     help_text='Person Entering the Data')
    institution = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="Institution",
                                   help_text='Name of Supplier, Bank, Contractor etc')
    description = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="Description")
    amount = models.DecimalField(max_digits=20, decimal_places=0, default=0, null = True, blank = True, verbose_name="Amount")
    accounts_debit = models.ForeignKey(AccountsDebit, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Accounts Debit')
    accounts_credit = models.ForeignKey(AccountsCredit, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Accounts Credit')

    def __str__(self):
        return self.employee_name

    def save(self, *args, **kwargs):
        if not self.custom_user:
            self.custom_user = self.request.user.username
        super().save(*args, **kwargs)
 
    class Meta:
        verbose_name = 'Bakery General Ledger'
        verbose_name_plural = 'Bakery General Ledger'


#############   #############   #############   #############   #############
#------------------------- Supermarket General Ledger  ---------------------#
#############   #############   #############   #############   #############

class SupermarketGeneralLedger(models.Model):
    created = models.DateField(default=now, verbose_name = "Date")
    department_name =  models.ForeignKey(Department, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Department')
    management_level = models.ForeignKey(ManagementLevel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Management Level",
                                         help_text='Management or Employee')
    employee_name = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="Employee Name", 
                                     help_text='Name of Employee Performing the Transaction')
    custom_user = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="User", 
                                     help_text='Person Entering the Data')
    institution = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="Institution",
                                   help_text='Name of Supplier, Bank, Contractor etc')
    description = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="Description")
    amount = models.DecimalField(max_digits=20, decimal_places=0, default=0, null = True, blank = True, verbose_name="Amount")
    accounts_debit = models.ForeignKey(AccountsDebit, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Accounts Debit')
    accounts_credit = models.ForeignKey(AccountsCredit, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Accounts Credit')

    def __str__(self):
        return self.employee_name
    def save(self, *args, **kwargs):
            if not self.custom_user:
                self.custom_user = self.request.user.username
            super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Supermarket General Ledger'
        verbose_name_plural = 'Supermarket General Ledger'
        

#############   #############   #############   #############   #############
#------------------------- Boulangerie General Ledger  ---------------------#
#############   #############   #############   #############   #############

class BoulangerieGeneralLedger(models.Model):
    created = models.DateField(default=now, verbose_name = "Date")
    department_name =  models.ForeignKey(Department, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Department')
    management_level = models.ForeignKey(ManagementLevel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Management Level",
                                         help_text='Management or Employee')
    employee_name = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="Employee Name", 
                                     help_text='Name of Employee Performing the Transaction')
    custom_user = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="User", 
                                     help_text='Person Entering the Data')
    institution = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="Institution",
                                   help_text='Name of Supplier, Bank, Contractor etc')
    description = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="Description")
    amount = models.DecimalField(max_digits=20, decimal_places=0, default=0, null = True, blank = True, verbose_name="Amount")
    accounts_debit = models.ForeignKey(AccountsDebit, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Accounts Debit')
    accounts_credit = models.ForeignKey(AccountsCredit, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Accounts Credit')

    def __str__(self):
        return self.employee_name
    def save(self, *args, **kwargs):
        if not self.custom_user:
            self.custom_user = self.request.user.username
        super().save(*args, **kwargs)
 
    class Meta:
        verbose_name = 'Boulangerie General Ledger'
        verbose_name_plural = 'Boulangerie General Ledger'
        
#############   #############   #############   #############   #############
#------------------------- Bar General Ledger  ---------------------#
#############   #############   #############   #############   #############
       
class BarGeneralLedger(models.Model):
    created = models.DateField(default=now, verbose_name = "Date")
    department_name =  models.ForeignKey(Department, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Department')
    management_level = models.ForeignKey(ManagementLevel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Management Level",
                                         help_text='Management or Employee')
    employee_name = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="Employee Name", 
                                     help_text='Name of Employee Performing the Transaction')
    custom_user = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="User", 
                                     help_text='Person Entering the Data')
    institution = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="Institution",
                                   help_text='Name of Supplier, Bank, Contractor etc')
    description = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="Description")
    amount = models.DecimalField(max_digits=20, decimal_places=0, default=0, null = True, blank = True, verbose_name="Amount")
    accounts_debit = models.ForeignKey(AccountsDebit, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Accounts Debit')
    accounts_credit = models.ForeignKey(AccountsCredit, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Accounts Credit')

    def __str__(self):
        return self.employee_name
    def save(self, *args, **kwargs):
        if not self.custom_user:
            self.custom_user = self.request.user.username
        super().save(*args, **kwargs)
 
    class Meta:
        verbose_name = 'Bar General Ledger'
        verbose_name_plural = 'Bar General Ledger'
        
        
        
class WholesaleGeneralLedger(models.Model):
    created = models.DateField(default=now, verbose_name = "Date")
    department_name =  models.ForeignKey(Department, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Department')
    management_level = models.ForeignKey(ManagementLevel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Management Level",
                                         help_text='Management or Employee')
    employee_name = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="Employee Name", 
                                     help_text='Name of Employee Performing the Transaction')
    custom_user = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="User", 
                                     help_text='Person Entering the Data')
    institution = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="Institution",
                                   help_text='Name of Supplier, Bank, Contractor etc')
    description = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name="Description")
    amount = models.DecimalField(max_digits=20, decimal_places=0, default=0, null = True, blank = True, verbose_name="Amount")
    accounts_debit = models.ForeignKey(AccountsDebit, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Accounts Debit')
    accounts_credit = models.ForeignKey(AccountsCredit, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Accounts Credit')

    def __str__(self):
        return self.employee_name
    def save(self, *args, **kwargs):
        if not self.custom_user:
            self.custom_user = self.request.user.username
        super().save(*args, **kwargs)
 
    class Meta:
        verbose_name = 'Wholesale General Ledger'
        verbose_name_plural = 'Wholesale General Ledger'