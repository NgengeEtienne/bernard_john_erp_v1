from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AccountsCategoryForm, AccountsSubCategoryForm, AccountsDebitForm, AccountsCreditForm, BakeryGeneralLedgerForm, SupermarketGeneralLedgerForm, BoulangerieGeneralLedgerForm, BarGeneralLedgerForm, WholesaleGeneralLedgerForm
from .models import AccountsCategory, AccountsSubCategory, AccountsDebit, AccountsCredit, BakeryGeneralLedger, SupermarketGeneralLedger, BoulangerieGeneralLedger, BarGeneralLedger, WholesaleGeneralLedger
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Department, ManagementLevel, AccountsDebit, AccountsCredit  # Import your models

# Create your views here.
 



@login_required
def accounting_view(request):
    # Your homepage logic (e.g., display featured content)
    return render(request, 'accounting/accounting.html')

@login_required
def accounts_category(request):
    accounts_category = AccountsCategory.objects.all()
    if request.method == 'POST':
        form = AccountsCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Accounts Category Added Successfully')
            return redirect('accounts_category')
    else:
        form = AccountsCategoryForm()
    context = {'accounts_category': accounts_category, 'form': form}
    return render(request, 'accounting/accounts_category.html', context)

@login_required
def accounts_category_edit(request, pk):
    category = get_object_or_404(AccountsCategory, pk=pk)
    if request.method == 'POST':
        form = AccountsCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Accounts Category Updated Successfully')
            return redirect('accounting:accounts_category')
    else:
        form = AccountsCategoryForm(instance=category)
    context = {'form': form}
    return render(request, 'accounting/accounts_category_edit.html', context)
#  Accounts SubCategory Views



def accounts_sub_category(request):
    sub_categories = AccountsSubCategory.objects.all()
    return render(request, 'accounting/accounts_sub_category.html', {'sub_categories': sub_categories})

def accounts_sub_category_add(request, pk=None):
    form = AccountsSubCategoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('accounting:accounts_sub_category')
    return render(request, 'accounting/accounts_sub_category_edit.html', {'form': form, 'edit': False})

def accounts_sub_category_edit(request, pk):
    sub_category = get_object_or_404(AccountsSubCategory, pk=pk)
    form = AccountsSubCategoryForm(request.POST or None, instance=sub_category)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('accounting:accounts_sub_category')
    return render(request, 'accounting/accounts_sub_category_edit.html', {'form': form, 'edit': True})

# Accounts Debit Views
def accounts_debit(request):
    debits = AccountsDebit.objects.all()
    return render(request, 'accounting/accounts_debit.html', {'debits': debits})

def accounts_debit_add(request, pk=None):
    form = AccountsDebitForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('accounting:accounts_debit')
    return render(request, 'accounting/accounts_debit_edit.html', {'form': form, 'edit': False})

def accounts_debit_edit(request, pk):
    debit = get_object_or_404(AccountsDebit, pk=pk)
    form = AccountsDebitForm(request.POST or None, instance=debit)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('accounting:accounts_debit')
    return render(request, 'accounting/accounts_debit_edit.html', {'form': form, 'edit': True})

# Accounts Credit Views
def accounts_credit(request):
    credits = AccountsCredit.objects.all()
    return render(request, 'accounting/accounts_credit.html', {'credits': credits})

def accounts_credit_add(request, pk=None):
    form = AccountsCreditForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('accounting:accounts_credit')
    return render(request, 'accounting/accounts_credit_edit.html', {'form': form, 'edit': False})

def accounts_credit_edit(request, pk):
    credit = get_object_or_404(AccountsCredit, pk=pk)
    form = AccountsCreditForm(request.POST or None, instance=credit)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('accounting:accounts_credit')
    return render(request, 'accounting/accounts_credit_edit.html', {'form': form, 'edit': True})












##################################ADD############################

@login_required

def accounts_category_add(request):
    """ Add a new accounts category """
    if request.method == 'POST':
        form = AccountsCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Accounts Category added successfully!')
            return redirect('accounting:accounts_category')
    else:
        form = AccountsCategoryForm()

    return render(request, 'accounting/accounts_category_edit.html', {'form': form})













@login_required
def general_ledger_view(request, department):
    general_ledger = globals()[f'{department.capitalize()}GeneralLedger'].objects.all()
    form = globals()[f'{department.capitalize()}GeneralLedgerForm']()
    context = {f'general_ledger': general_ledger, 'form': form, 'department': department}
    return render(request, 'accounting/general_ledger.html', context)

@login_required
def general_ledger_edit(request, department, pk):
    # Get the general ledger instance
    general_ledger = globals()[f'{department.capitalize()}GeneralLedger'].objects.get(pk=pk)
    # form = globals()[f'{department.capitalize()}GeneralLedgerForm'](request.POST, instance=general_ledger)
    
    if request.method == 'POST':
        form = globals()[f'{department.capitalize()}GeneralLedgerForm'](request.POST, instance=general_ledger)
        general_ledger_model = globals().get(f'{department.capitalize()}GeneralLedger')
        
        if form.is_valid():
            # Save the form first to update the general ledger record
            form.save()
            
            # Initialize total amount
            total = 0
            row_count = int(request.POST.get("row_count", 0))
            
            if row_count:
                # Process each row of data
                for i in range(1, row_count + 1):
                    print("Processing row", i)
                    
                    # Extract row-specific data
                    created_row = request.POST.get(f'created_{i}')
                    management_level_id_row = request.POST.get(f'management_level_{i}')
                    employee_name_row = request.POST.get(f'employee_name_{i}')
                    institution_row = request.POST.get(f'institution_{i}')
                    description_row = request.POST.get(f'description_{i}')
                    amount_row = request.POST.get(f'amount_{i}')
                    accounts_debit_id_row = request.POST.get(f'accounts_debit_{i}')
                    accounts_credit_id_row = request.POST.get(f'accounts_credit_{i}')
                    
                    # Print row-specific data
                    print(f"Row {i} - Created: {created_row}")
                    print(f"Row {i} - Management Level ID: {management_level_id_row}")
                    print(f"Row {i} - Employee Name: {employee_name_row}")
                    print(f"Row {i} - Institution: {institution_row}")
                    print(f"Row {i} - Description: {description_row}")
                    print(f"Row {i} - Amount: {amount_row}")
                    print(f"Row {i} - Accounts Debit ID: {accounts_debit_id_row}")
                    print(f"Row {i} - Accounts Credit ID: {accounts_credit_id_row}")
                    
                    if amount_row:
                        # Calculate row total
                        row_total = float(amount_row)
                        total += row_total
                        
                        # Update or create ledger detail
                        detail_id = request.POST.get(f'detail_id_{i}')
                        if detail_id:
                            detail = general_ledger_model.objects.get(id=detail_id)
                            detail.created = created_row
                            detail.management_level = get_object_or_404(ManagementLevel, pk=management_level_id_row) if management_level_id_row else None
                            detail.employee_name = employee_name_row
                            detail.institution = institution_row
                            detail.description = description_row
                            detail.amount = amount_row
                            detail.accounts_debit = get_object_or_404(AccountsDebit, pk=accounts_debit_id_row) if accounts_debit_id_row else None
                            detail.accounts_credit = get_object_or_404(AccountsCredit, pk=accounts_credit_id_row) if accounts_credit_id_row else None
                            detail.save()
                            print(f"Updated detail for row {i}:", detail)
                        else:
                            # If detail_id is not present, create a new detail
                            detail = general_ledger_model.objects.create(
                                created=created_row,
                                department_name=get_object_or_404(Department, department_name=department.capitalize()),
                                management_level=get_object_or_404(ManagementLevel, pk=management_level_id_row) if management_level_id_row else None,
                                employee_name=employee_name_row,
                                custom_user=request.user.username,
                                institution=institution_row,
                                description=description_row,
                                amount=amount_row,
                                accounts_debit=get_object_or_404(AccountsDebit, pk=accounts_debit_id_row) if accounts_debit_id_row else None,
                                accounts_credit=get_object_or_404(AccountsCredit, pk=accounts_credit_id_row) if accounts_credit_id_row else None
                            )
                            print(f"Saved detail for row {i}:", detail)
                
                # Save the total amount
                general_ledger.total_amount = total
                general_ledger.save()
                print("Total amount saved:", general_ledger.total_amount)

            return JsonResponse({"success": True, "ledger_id": general_ledger.id})
        else:
            return JsonResponse({"success": False, "error": form.errors})
    
    # Fetch existing rows for this ledger
    form = globals()[f'{department.capitalize()}GeneralLedgerForm'](instance=general_ledger)
    rows = globals()[f'{department.capitalize()}GeneralLedger'].objects.filter(pk=pk)
    
    context = {
        'form': form,
        'department': department,
        'rows': rows,
    }
    return render(request, 'accounting/general_ledger_edit.html', context)

@login_required


def general_ledger_add(request, department):
    model_class = globals().get(f'{department.capitalize()}GeneralLedger')
    form_class = globals().get(f'{department.capitalize()}GeneralLedgerForm')

    if request.method == "POST":
        general_ledger_model = globals().get(f'{department.capitalize()}GeneralLedger')
        # Initialize total amount
        total = 0
        row_count = int(request.POST.get("row_count", 0))
        if row_count:
            # Process each row of data
            
            print("Row count:", row_count)
            
            for i in range(1, row_count + 1):
                print("Processing row", i)
                
                # Extract row-specific data
                created_row = request.POST.get(f'created_{i}')
                management_level_id_row = request.POST.get(f'management_level_{i}')
                employee_name_row = request.POST.get(f'employee_name_{i}')
                institution_row = request.POST.get(f'institution_{i}')
                description_row = request.POST.get(f'description_{i}')
                amount_row = request.POST.get(f'amount_{i}')
                accounts_debit_id_row = request.POST.get(f'accounts_debit_{i}')
                accounts_credit_id_row = request.POST.get(f'accounts_credit_{i}')
                
                # Print row-specific data
                print(f"Row {i} - Created: {created_row}")
                print(f"Row {i} - Management Level ID: {management_level_id_row}")
                print(f"Row {i} - Employee Name: {employee_name_row}")
                print(f"Row {i} - Institution: {institution_row}")
                print(f"Row {i} - Description: {description_row}")
                print(f"Row {i} - Amount: {amount_row}")
                print(f"Row {i} - Accounts Debit ID: {accounts_debit_id_row}")
                print(f"Row {i} - Accounts Credit ID: {accounts_credit_id_row}")
                
                if amount_row:
                    # Calculate row total
                    row_total = float(amount_row)
                    total += row_total
                    
                    # Create and save the ledger detail
                    detail = general_ledger_model.objects.create(
                        created=created_row,
                        department_name=get_object_or_404(Department, department_name=department.capitalize()),
                        management_level=get_object_or_404(ManagementLevel, pk=management_level_id_row) if management_level_id_row else None,
                        employee_name=employee_name_row,
                        custom_user=request.user.username,
                        institution=institution_row,
                        description=description_row,
                        amount=amount_row,
                        accounts_debit=get_object_or_404(AccountsDebit, pk=accounts_debit_id_row) if accounts_debit_id_row else None,
                        accounts_credit=get_object_or_404(AccountsCredit, pk=accounts_credit_id_row) if accounts_credit_id_row else None
                    )
                    print(f"Saved detail for row {i}:", detail)
            
            # Save the total amount
            
            detail.save()
            print("Total amount saved:", detail.amount)

            return JsonResponse({"success": True, "ledger_id": detail.id})

        else:
            print("Error: Missing required data")
            return JsonResponse({"success": False, "error": "Missing required data"})
    else:
        form = form_class()
        context = {'form': form, 'department': department}
        return render(request, 'accounting/general_ledger_add.html', context)

from django.template.loader import render_to_string
from django.http import JsonResponse
def add_more_row(request,department):
    form_class = globals().get(f'{department.capitalize()}GeneralLedgerForm')
        
    if not form_class:
        return JsonResponse({'error': 'Form not found'}, status=400)
    
    form = form_class()
    
    
    # Render the form row template
    rendered_row = render_to_string('accounting/general_ledger_row.html', {'form': form}, request=request)
    
    return JsonResponse({'row_html': rendered_row})

 