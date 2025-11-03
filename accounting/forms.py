from django import forms
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django import forms
from django.forms import modelformset_factory
from .models import AccountsCategory, AccountsSubCategory, AccountsDebit, AccountsCredit, BakeryGeneralLedger, SupermarketGeneralLedger, BoulangerieGeneralLedger, BarGeneralLedger, WholesaleGeneralLedger
class AccountsCategoryForm(forms.ModelForm):
    class Meta:
        model = AccountsCategory
        fields = ['account_category']
        labels = {
            'account_category': 'Accounts Category',
        }
        widgets = {
            'account_category': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'account_category',
                'placeholder': 'Enter Accounts Category',
                'required': 'required',  # Make the field required
            }),
        }

class AccountsSubCategoryForm(forms.ModelForm):
    class Meta:
        model = AccountsSubCategory
        fields = ['account_sub_category', 'accounts_category']
        labels = {
            'account_sub_category': 'Accounts Sub Category',
            'accounts_category': 'Accounts Category',
        }
        widgets = {
            'account_sub_category': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'account_sub_category',
                'placeholder': 'Enter Accounts Sub Category',
                'required': 'required',  # Make the field required
            }),
            'accounts_category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_category',
            }),
        }

class AccountsDebitForm(forms.ModelForm):
    class Meta:
        model = AccountsDebit
        fields = ['account_debit', 'accounts_sub_category']
        labels = {
            'account_debit': 'Accounts Debit',
            'accounts_sub_category': 'Accounts Sub Category',
        }
        widgets = {
            'account_debit': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'account_debit',
                'placeholder': 'Enter Accounts Debit',
                'required': 'required',  # Make the field required
            }),
            'accounts_sub_category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_sub_category',
            }),
        }

class AccountsCreditForm(forms.ModelForm):
    class Meta:
        model = AccountsCredit
        fields = ['account_credit', 'accounts_sub_category']
        labels = {
            'account_credit': 'Accounts Credit',
            'accounts_sub_category': 'Accounts Sub Category',
        }
        widgets = {
            'account_credit': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'account_credit',
                'placeholder': 'Enter Accounts Credit',
                'required': 'required',  # Make the field required
            }),
            'accounts_sub_category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_sub_category',
            }),
        }

class BakeryGeneralLedgerForm(forms.ModelForm):
    class Meta:
        model = BakeryGeneralLedger
        fields = ['created', 'department_name', 'management_level', 'employee_name', 'custom_user', 'institution', 'description', 'amount', 'accounts_debit', 'accounts_credit']
        labels = {
            'created': 'Date',
            'department_name': 'Department',
            'management_level': 'Management Level',
            'employee_name': 'Employee Name',
            'custom_user': 'User',
            'institution': 'Institution',
            'description': 'Description',
            'amount': 'Amount',
            'accounts_debit': 'Accounts Debit',
            'accounts_credit': 'Accounts Credit',
        }
        widgets = {
            'created': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'created',
                'placeholder': 'Enter Date',
                'required': 'required',  # Make the field required
           'type':'date',
 }),
            'department_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'department_name',
                'placeholder': 'Enter Department Name',
                'required': 'required',  # Make the field required
            }),
            'management_level': forms.Select(attrs={
                'class': 'form-control',
                'id': 'management_level',
            }),
            'employee_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'employee_name',
                'placeholder': 'Enter Employee Name',
                'required': 'required',  # Make the field required
            }),
            'custom_user': forms.Select(attrs={
                'class': 'form-control',
                'id': 'custom_user',
            }),
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'institution',
                'placeholder': 'Enter Institution',
                'required': 'required',  # Make the field required
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'description',
                'placeholder': 'Enter Description',
                'required': 'required',  # Make the field required
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'amount',
                'placeholder': 'Enter Amount',
                'required': 'required',  # Make the field required
            }),
            'accounts_debit': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_debit',
            }),
            'accounts_credit': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_credit',
            }),
        }

class SupermarketGeneralLedgerForm(forms.ModelForm):
    class Meta:
        model = SupermarketGeneralLedger
        fields = ['created', 'department_name', 'management_level', 'employee_name', 'custom_user', 'institution', 'description', 'amount', 'accounts_debit', 'accounts_credit']
        labels = {
            'created': 'Date',
            'department_name': 'Department',
            'management_level': 'Management Level',
            'employee_name': 'Employee Name',
            'custom_user': 'User',
            'institution': 'Institution',
            'description': 'Description',
            'amount': 'Amount',
            'accounts_debit': 'Accounts Debit',
            'accounts_credit': 'Accounts Credit',
        }
        widgets = {
            'created': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'created',
                'placeholder': 'Enter Date',
                'required': 'required',  # Make the field required
           'type':'date',
 }),
            'department_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'department_name',
                'placeholder': 'Enter Department Name',
                'required': 'required',  # Make the field required
            }),
            'management_level': forms.Select(attrs={
                'class': 'form-control',
                'id': 'management_level',
            }),
            'employee_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'employee_name',
                'placeholder': 'Enter Employee Name',
                'required': 'required',  # Make the field required
            }),
            'custom_user': forms.Select(attrs={
                'class': 'form-control',
                'id': 'custom_user',
            }),
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'institution',
                'placeholder': 'Enter Institution',
                'required': 'required',  # Make the field required
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'description',
                'placeholder': 'Enter Description',
                'required': 'required',  # Make the field required
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'amount',
                'placeholder': 'Enter Amount',
                'required': 'required',  # Make the field required
            }),
            'accounts_debit': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_debit',
            }),
            'accounts_credit': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_credit',
            }),
        }

class BoulangerieGeneralLedgerForm(forms.ModelForm):
    class Meta:
        model = BoulangerieGeneralLedger
        fields = ['created', 'department_name', 'management_level', 'employee_name', 'custom_user', 'institution', 'description', 'amount', 'accounts_debit', 'accounts_credit']
        labels = {
            'created': 'Date',
            'department_name': 'Department',
            'management_level': 'Management Level',
            'employee_name': 'Employee Name',
            'custom_user': 'User',
            'institution': 'Institution',
            'description': 'Description',
            'amount': 'Amount',
            'accounts_debit': 'Accounts Debit',
            'accounts_credit': 'Accounts Credit',
        }
        widgets = {
            'created': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'created',
                'placeholder': 'Enter Date',
                'required': 'required',  # Make the field required
           'type':'date',
 }),
            'department_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'department_name',
                'placeholder': 'Enter Department Name',
                'required': 'required',  # Make the field required
            }),
            'management_level': forms.Select(attrs={
                'class': 'form-control',
                'id': 'management_level',
                'placeholder': 'Select Management Level',
                'required': 'required',  # Make the field required
            }),
            'employee_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'employee_name',
                'placeholder': 'Enter Employee Name',
                'required': 'required',  # Make the field required
            }),
            'custom_user': forms.Select(attrs={
                'class': 'form-control',
                'id': 'custom_user',
                'placeholder': 'Select User',
                'required': 'required',  # Make the field required
            }),
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'institution',
                'placeholder': 'Enter Institution',
                'required': 'required',  # Make the field required
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'description',
                'placeholder': 'Enter Description',
                'required': 'required',  # Make the field required
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'amount',
                'placeholder': 'Enter Amount',
                'required': 'required',  # Make the field required
            }),
            'accounts_debit': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_debit',
                'placeholder': 'Select Accounts Debit',
                'required': 'required',  # Make the field required
            }),
            'accounts_credit': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_credit',
                'placeholder': 'Select Accounts Credit',
                'required': 'required',  # Make the field required
            }),
        }


class SupermarketGeneralLedgerForm(forms.ModelForm):
    class Meta:
        model = SupermarketGeneralLedger
        fields = ['created', 'department_name', 'management_level', 'employee_name', 'custom_user', 'institution', 'description', 'amount', 'accounts_debit', 'accounts_credit']
        labels = {
            'created': 'Date',
            'department_name': 'Department',
            'management_level': 'Management Level',
            'employee_name': 'Employee Name',
            'custom_user': 'User',
            'institution': 'Institution',
            'description': 'Description',
            'amount': 'Amount',
            'accounts_debit': 'Accounts Debit',
            'accounts_credit': 'Accounts Credit',
        }
        widgets = {
            'created': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'created',
                'placeholder': 'Enter Date',
                'required': 'required',  # Make the field required
           'type':'date',
 }),
            'department_name': forms.Select(attrs={
                'class': 'form-control',
                'id': 'department_name',
                'placeholder': 'Select Department',
                'required': 'required',  # Make the field required
            }),
            'management_level': forms.Select(attrs={
                'class': 'form-control',
                'id': 'management_level',
                'placeholder': 'Select Management Level',
                'required': 'required',  # Make the field required
            }),
            'employee_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'employee_name',
                'placeholder': 'Select Employee',
                'required': 'required',  # Make the field required
            }),
            'custom_user': forms.Select(attrs={
                'class': 'form-control',
                'id': 'custom_user',
                'placeholder': 'Select User',
                'required': 'required',  # Make the field required
            }),
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'institution',
                'placeholder': 'Enter Institution',
                'required': 'required',  # Make the field required
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'description',
                'placeholder': 'Enter Description',
                'required': 'required',  # Make the field required
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'amount',
                'placeholder': 'Enter Amount',
                'required': 'required',  # Make the field required
            }),
            'accounts_debit': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_debit',
                'placeholder': 'Select Accounts Debit',
                'required': 'required',  # Make the field required
            }),
            'accounts_credit': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_credit',
                'placeholder': 'Select Accounts Credit',
                'required': 'required',  # Make the field required
            }),
        }


class BoulangerieGeneralLedgerForm(forms.ModelForm):
    class Meta:
        model = BoulangerieGeneralLedger
        fields = ['created', 'department_name', 'management_level', 'employee_name', 'custom_user', 'institution', 'description', 'amount', 'accounts_debit', 'accounts_credit']
        labels = {
            'created': 'Date',
            'department_name': 'Department',
            'management_level': 'Management Level',
            'employee_name': 'Employee Name',
            'custom_user': 'User',
            'institution': 'Institution',
            'description': 'Description',
            'amount': 'Amount',
            'accounts_debit': 'Accounts Debit',
            'accounts_credit': 'Accounts Credit',
        }
        widgets = {
            'created': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'created',
                'placeholder': 'Enter Date',
                'required': 'required',  # Make the field required
           'type':'date',
 }),
            'department_name': forms.Select(attrs={
                'class': 'form-control',
                'id': 'department_name',
                'placeholder': 'Select Department',
                'required': 'required',  # Make the field required
            }),
            'management_level': forms.Select(attrs={
                'class': 'form-control',
                'id': 'management_level',
                'placeholder': 'Select Management Level',
                'required': 'required',  # Make the field required
            }),
            'employee_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'employee_name',
                'placeholder': 'Select Employee',
                'required': 'required',  # Make the field required
            }),
            'custom_user': forms.Select(attrs={
                'class': 'form-control',
                'id': 'custom_user',
                'placeholder': 'Select User',
                'required': 'required',  # Make the field required
            }),
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'institution',
                'placeholder': 'Enter Institution',
                'required': 'required',  # Make the field required
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'description',
                'placeholder': 'Enter Description',
                'required': 'required',  # Make the field required
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'amount',
                'placeholder': 'Enter Amount',
                'required': 'required',  # Make the field required
            }),
            'accounts_debit': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_debit',
                'placeholder': 'Select Accounts Debit',
                'required': 'required',  # Make the field required
            }),
            'accounts_credit': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_credit',
                'placeholder': 'Select Accounts Credit',
                'required': 'required',  # Make the field required
            }),
        }


class BarGeneralLedgerForm(forms.ModelForm):
    class Meta:
        model = BarGeneralLedger
        fields = ['created', 'department_name', 'management_level', 'employee_name', 'custom_user', 'institution', 'description', 'amount', 'accounts_debit', 'accounts_credit']
        labels = {
            'created': 'Date',
            'department_name': 'Department',
            'management_level': 'Management Level',
            'employee_name': 'Employee Name',
            'custom_user': 'User',
            'institution': 'Institution',
            'description': 'Description',
            'amount': 'Amount',
            'accounts_debit': 'Accounts Debit',
            'accounts_credit': 'Accounts Credit',
        }
        widgets = {
            'created': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'created',
                'placeholder': 'Enter Date',
                'required': 'required',  # Make the field required
           'type':'date',
 }),
            'department_name': forms.Select(attrs={
                'class': 'form-control',
                'id': 'department_name',
                'placeholder': 'Select Department',
                'required': 'required',  # Make the field required
            }),
            'management_level': forms.Select(attrs={
                'class': 'form-control',
                'id': 'management_level',
                'placeholder': 'Select Management Level',
                'required': 'required',  # Make the field required
            }),
            'employee_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'employee_name',
                'placeholder': 'Select Employee',
                'required': 'required',  # Make the field required
            }),
            'custom_user': forms.Select(attrs={
                'class': 'form-control',
                'id': 'custom_user',
                'placeholder': 'Select User',
                'required': 'required',  # Make the field required
            }),
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'institution',
                'placeholder': 'Enter Institution',
                'required': 'required',  # Make the field required
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'description',
                'placeholder': 'Enter Description',
                'required': 'required',  # Make the field required
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'amount',
                'placeholder': 'Enter Amount',
                'required': 'required',  # Make the field required
            }),
            'accounts_debit': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_debit',
                'placeholder': 'Select Accounts Debit',
                'required': 'required',  # Make the field required
            }),
            'accounts_credit': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_credit',
                'placeholder': 'Select Accounts Credit',
                'required': 'required',  # Make the field required
            }),
        }


class WholesaleGeneralLedgerForm(forms.ModelForm):
    class Meta:
        model = WholesaleGeneralLedger
        fields = ('created', 'department_name', 'management_level', 'employee_name', 'custom_user', 'institution', 'description', 'amount', 'accounts_debit', 'accounts_credit')

        widgets = {
            'created': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'created',
                'placeholder': 'Select Date',
                'required': 'required',  # Make the field required
            }),
            'department_name': forms.Select(attrs={
                'class': 'form-control',
                'id': 'department_name',
                'placeholder': 'Select Department',
                'required': 'required',  # Make the field required
            }),
            'management_level': forms.Select(attrs={
                'class': 'form-control',
                'id': 'management_level',
                'placeholder': 'Select Management Level',
                'required': 'required',  # Make the field required
            }),
            'employee_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'employee_name',
                'placeholder': 'Select Employee',
                'required': 'required',  # Make the field required
            }),
            'custom_user': forms.Select(attrs={
                'class': 'form-control',
                'id': 'custom_user',
                'placeholder': 'Select User',
                'required': 'required',  # Make the field required
            }),
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'institution',
                'placeholder': 'Enter Institution',
                'required': 'required',  # Make the field required
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'description',
                'placeholder': 'Enter Description',
                'required': 'required',  # Make the field required
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'amount',
                'placeholder': 'Enter Amount',
                'required': 'required',  # Make the field required
            }),
            'accounts_debit': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_debit',
                'placeholder': 'Select Accounts Debit',
                'required': 'required',  # Make the field required
            }),
            'accounts_credit': forms.Select(attrs={
                'class': 'form-control',
                'id': 'accounts_credit',
                'placeholder': 'Select Accounts Credit',
                'required': 'required',  # Make the field required
            }),
        }

