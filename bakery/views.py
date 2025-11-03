from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from django.views.generic.detail import DetailView

from django.urls import reverse_lazy
from django.contrib import messages

from django.contrib.messages.views import SuccessMessageMixin

#from .forms import *
from django.db.models import Sum
from django.db.models import Q
from decimal import Decimal

from django.utils import timezone
from datetime import datetime

from django.utils.dateparse import parse_date
from .models import BakeryProduction, BakeryRawMaterialUsage, BakeryProductionOutput


from .models import *
from customer.models import *
from product.models import *
# Create your views here.
from configuration.models import Department
from .forms import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Invoice view


@login_required
def bakery_view(request):
    # Your homepage logic (e.g., display featured content)
    return render(request, 'bakery/bakery.html')




class BakeryProductListView(ListView):
    model = BakeryProduct
    template_name = 'bakery/product/list.html'
    context_object_name = 'products'

class BakeryProductCreateView(CreateView):
    model = BakeryProduct
    template_name = 'bakery/product/add.html'
    fields = '__all__'  # or specify the fields you want to include
    success_url = reverse_lazy('bakery:product-list')  # Redirect after successful creation

class BakeryProductUpdateView(UpdateView):
    model = BakeryProduct
    template_name = 'bakery/product/add.html'
    fields = '__all__'  # or specify the fields you want to include
    success_url = reverse_lazy('bakery:product-list')  # Redirect after successful update



from django.views.generic import ListView, CreateView, UpdateView
from .models import ProductRecipe

class ProductRecipeListView(ListView):
    model = ProductRecipe
    template_name = 'bakery/recipe/list.html'
    context_object_name = 'product_recipes'

class ProductRecipeCreateView(CreateView):
    model = ProductRecipe
    template_name = 'bakery/recipe/add_edit.html'
    fields = ['product', 'recipe', 'quantity_per_product']

    def form_valid(self, form):
        form.save()
        return redirect('bakery:productrecipe-list')


class ProductRecipeUpdateView(UpdateView):
    model = ProductRecipe
    template_name = 'bakery/recipe/add_edit.html'
    fields = ['product', 'recipe', 'quantity_per_product']

    def form_valid(self, form):
        form.save()
        return redirect('bakery:productrecipe-list')



#Raw materials
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .models import RawMaterials

class RawMaterialsListView(ListView):
    model = RawMaterials
    template_name = 'bakery/raw_materials/list.html'
    context_object_name = 'raw_materials'

class RawMaterialsCreateView(CreateView):
    model = RawMaterials
    template_name = 'bakery/raw_materials/add_edit.html'
    fields = '__all__'

    def form_valid(self, form):
        form.save()
        return redirect('bakery:raw-materials-list')

class RawMaterialsUpdateView(UpdateView):
    model = RawMaterials
    template_name = 'bakery/raw_materials/add_edit.html'
    fields = '__all__'

    def form_valid(self, form):
        form.save()
        return redirect('bakery:raw-materials-list')


#ecipe raw materials
from django.views.generic import ListView, CreateView, UpdateView
from .models import RecipeRawMaterial
from django.views.generic import ListView
from django.db.models import Sum, Count
from .models import Recipe, RecipeRawMaterial


def recipe_raw_material_list_view(request):
    # Fetch recipes with annotations for raw material count and total quantity
    recipes = (
        Recipe.objects
        .annotate(
            raw_material_count=Count('reciperawmaterial'),
            total_quantity=Sum('reciperawmaterial__quantity_per_recipe')
        )
    )
    # print("recipes: ", recipes)

    # Fetch all raw materials to display in modals
    recipe_raw_materials = RecipeRawMaterial.objects.select_related('raw_material', 'recipe')
    print("recipe raw materials: ", recipe_raw_materials)
    # Pass the context to the template
    context = {
        'recipes': recipes,
        'recipe_raw_materials': recipe_raw_materials,
    }

    return render(request, 'bakery/reciperawmaterials/list.html', context)


@login_required
def create_recipe_raw_material(request):

    form = RecipeRawMaterial()
    formset = RecipeRawMaterialFormSet(queryset=RecipeRawMaterial.objects.none()) 
    if request.method == "POST":
        
        recipe_id=int(request.POST.get("form-0-recipe"))
        
        # department = Department.objects.filter(department_name="Bakery").first()  # Set the department to "Bakery"
        # employee = request.POST.get("employee")
        print(f"recipe_id (before conversion): {recipe_id}")
        # print(f"department (after conversion): {department}")
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        print(f"recipe: {recipe}")
       
        if recipe:
            row_count = int(request.POST.get("row_count", 0))  # Number of rows
            print("row gotten: ", row_count)
            for i in range(1, row_count + 1):
                print("in for loop")
                product_id = request.POST.get(f"raw_material{i}")
                quantity = Decimal(request.POST.get(f"quantity_{i}", 0))
                measure = request.POST.get(f"measure_{i}", 0)
                # discount_price = float(request.POST.get(f"discount_amount_{i}", 0))

                product = get_object_or_404(RawMaterials, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, measure: {measure}")

                if  product and quantity and measure:
                    # Calculate the sum for each row
                    
                    # Create and save the BakeryInvoiceDetail
                    detail = RecipeRawMaterial.objects.create(
                        recipe=recipe,
                        raw_material=product,
                        quantity_per_recipe=quantity,
                        measure=measure,
                    )
                    print(f"Saved detail for row {i}:", detail)

            
           

            # Optionally, return a JSON response indicating success
            return JsonResponse({"success": True, "invoice_id": detail.id})

        else:
            print("Error: Missing required invoice data")
            return JsonResponse({"success": False, "error": "Missing required invoice data"})

        #return redirect("bakery:purchases")

    context = {

        #"total_invoice": total_invoice,
        "form": form,
        "formset": formset,
    }

    return render(request, 'bakery/reciperawmaterials/add_edit.html', context)
#--------------------------------------------------------------------#

@login_required
def edit_recipe_raw_material(request, pk):
    # Fetch the existing invoice and its items
 
    # recipe=Recipe.objects.filter(pk=pk).first()
    recipe = Recipe.objects.filter(pk=pk)
    print(f"recipe: {recipe}")
    raw_mat=RecipeRawMaterial.objects.filter(recipe=pk)
    RecipeRawMaterialFormSet = modelformset_factory(RecipeRawMaterial, form=RecipeRawMaterialForm, extra=0, can_delete=True)

    # Initialize the forms with existing invoice data
    form = RecipeRawMaterial()
    formset = RecipeRawMaterialFormSet(
        queryset=raw_mat
    )

    if request.method == "POST":
        
        recipe_id=int(request.POST.get("form-0-recipe"))
        
        
        # department = Department.objects.filter(department_name="Bakery").first()  # Set the department to "Bakery"
        # employee = request.POST.get("employee")
        print(f"recipe_id (before conversion): {recipe_id}")
        # print(f"department (after conversion): {department}")
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        print(f"recipe: {recipe}")
       
        if recipe:
            row_count = int(request.POST.get("row_count", 0))  # Number of rows
            print("row gotten: ", row_count)
            for i in range(1, row_count + 1):
                raw_mat_id=int(request.POST.get(f"id_{i}",0))
                detail = raw_mat_id and get_object_or_404(RecipeRawMaterial, pk=raw_mat_id) or None
                print(f"detail: {detail}")
                print("in for loop")
                product_id = request.POST.get(f"raw_material{i}")
                quantity = Decimal(request.POST.get(f"quantity_{i}", 0))
                measure = request.POST.get(f"measure_{i}", 0)
                # discount_price = float(request.POST.get(f"discount_amount_{i}", 0))

                product = get_object_or_404(RawMaterials, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, measure: {measure}")

                if  product and quantity and measure:
                    # Calculate the sum for each row
                    if detail is not None:
                        # Update existing detail
                        detail = detail
                        detail.raw_material = product
                        detail.quantity_per_recipe = quantity
                        detail.measure = measure
                        detail.save()
                        print(f"Updated detail for row {i}: {detail}")
                    else:
                        # If there are fewer details than rows, create new ones
                        detail = RecipeRawMaterial.objects.create(
                        recipe=recipe,
                        raw_material=product,
                        quantity_per_recipe=quantity,
                        measure=measure,
                        )
                        print(f"Created new detail for row {i}: {detail}")

                    

            
           

            # Optionally, return a JSON response indicating success
            return JsonResponse({"success": True, "invoice_id": detail.id})

        else:
            print("Error: Missing required invoice data")
            return JsonResponse({"success": False, "error": "Missing required invoice data"})

        #return redirect("bakery:purchases")

            
    context = {
        "form": form,
        "formset": formset,
        "recipe": pk,
        "raw_mat":raw_mat,#pass the id of the raw mats
    }

    return render(request, "bakery/reciperawmaterials/add_edit.html", context)

#############   #############   #############   #############   #############
#------------------------- Customer Views ------------------------------#
#############   #############   #############   #############   #############
class BakeryCustomerListView(ListView):
    model = BakeryCustomer
    template_name = 'bakery/bakery_customer/customers.html'  # Specify your template name
    context_object_name = 'customers'  # The name to use in the template
    paginate_by = 1000  # Number of customers per page

    def get_queryset(self):
        return BakeryCustomer.objects.all().order_by('customer_name')  # Order by customer name

    
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
from bakery.models import BakeryCustomer, BakeryInvoice, BakeryInvoicePayment, BakeryCustomerOpeningBalance
from django.views.generic import DetailView
from django.http import HttpResponse
import csv

class BakeryCustomerDetailView(DetailView):
    model = BakeryCustomer
    template_name = 'bakery/bakery_customer/customer_account.html'
    context_object_name = 'customer'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        customer = get_object_or_404(BakeryCustomer, slug=slug)

        # Get the filter inputs from the request GET parameters
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        invoice_number = self.request.GET.get('invoice_number')
        status = self.request.GET.get('status')

        # Filter invoices for the customer and 'Sales' status
        invoices = BakeryInvoice.objects.filter(customer=customer, status='Sales')

        # Apply date range filter if both start and end dates are provided
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                invoices = invoices.filter(created__range=(start_date, end_date))
            except ValueError:
                pass  # Handle invalid date format if necessary

        # Apply filter for invoice number if provided
        if invoice_number:
            invoices = invoices.filter(invoice_id__icontains=invoice_number)

        # Apply filter for status if provided
        if status:
            invoices = invoices.filter(status=status)

        # Aggregate totals for invoices
        total_vat = invoices.aggregate(Sum('vat_amount'))['vat_amount__sum']
        total_discount = invoices.aggregate(Sum('bakeryinvoicedetail__discount_value'))['bakeryinvoicedetail__discount_value__sum']
        net_total = invoices.aggregate(Sum('bakeryinvoicedetail__net_amount'))['bakeryinvoicedetail__net_amount__sum']
        total_invoices = invoices.aggregate(Sum('invoice_total'))['invoice_total__sum']

        # Filter returns based on customer and 'Return Inwards' status
        returns = BakeryInvoice.objects.filter(customer=customer, status='Return Inwards')

        # Aggregate totals for returns
        total_returns = returns.aggregate(Sum('invoice_total'))['invoice_total__sum']

        # Filter payments for the customer
        payments = BakeryInvoicePayment.objects.filter(invoice__customer=customer)
        total_payments = payments.aggregate(Sum('amount_paid'))['amount_paid__sum']
        opening_balance = BakeryCustomerOpeningBalance.objects.filter(customer=customer).aggregate(Sum('amount_owed'))['amount_owed__sum']

        # Convert None values to Decimal(0) for calculations
        total_returns = Decimal(total_returns) if total_returns is not None else Decimal(0)
        total_payments = Decimal(total_payments) if total_payments is not None else Decimal(0)
        total_invoices = Decimal(total_invoices) if total_invoices is not None else Decimal(0)
        total_discount = Decimal(total_discount) if total_discount is not None else Decimal(0)
        opening_balance = Decimal(opening_balance) if opening_balance is not None else Decimal(0)
        net_total = Decimal(net_total) if net_total is not None else Decimal(0)

        # Calculate the account balance
        account_balance = total_invoices - total_discount - total_returns - total_payments + opening_balance

        # Add filtered invoices and returns to context
        self.extra_context = {
            'returns': returns,
            'invoices': invoices,
            'payments': payments,
            'total_returns': total_returns,
            'total_invoices': total_invoices,
            'total_payments': total_payments,
            'total_vat': total_vat,
            'opening_balance': opening_balance,
            'account_balance': account_balance,
            'total_discount': total_discount,
            "net_total": net_total,
        }

        return customer


    
class BakeryCustomerCreateView(View):
    def get(self, request):
        form = BakeryCustomerForm()
        return render(request, 'bakery/bakery_customer/add_customer_form.html', {'form': form})

    def post(self, request):
        form = BakeryCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bakery:customer')  # Redirect to customer list after successful creation
        return render(request, 'bakery/bakery_customer/add_customer_form.html', {'form': form})  
    
class BakeryCustomerEditView(UpdateView):
    model = BakeryCustomer
    form_class = BakeryCustomerForm
    template_name = 'bakery/bakery_customer/edit_customer_form.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(BakeryCustomer, slug=slug)

    def form_valid(self, form):
        form.save()
        return redirect('bakery:customer')  # Redirect to the customer list after saving    
    
#############   #############   #############   #############   #############
#------------------------- Product Views ------------------------------#
#############   #############   #############   #############   ############# 
class BakeryProductCategoryListView(ListView):
    model = BakeryProductCategory
    template_name = 'bakery/bakery_product/categories.html'  # Specify your template name
    context_object_name = 'categories'  # The name to use in the template
    paginate_by = 10  # Number of categories per page

    def get_queryset(self):
        return BakeryProductCategory.objects.all().order_by('category_name')  # Order by category name


class BakeryProductCategoryDetailView(DetailView):
    model = BakeryProductCategory
    template_name = 'bakery/bakery_product/category_detail.html'  # Specify your template name
    context_object_name = 'category'  # The name to use in the template
    slug_field = 'slug'  # Use slug field for URL lookup
    slug_url_kwarg = 'slug'  # The name of the slug URL parameter


class BakeryProductCategoryCreateView(CreateView):
    model = BakeryProductCategory
    form_class = BakeryProductCategoryForm  # Ensure you have a form for this model
    template_name = 'bakery/bakery_product/add_category_form.html'  # Specify your template name

    def form_valid(self, form):
        form.save()
        return redirect('bakery:category-list')  # Redirect to category list after successful creation
    


class BakeryProductCategoryEditView(UpdateView):
    model = BakeryProductCategory
    form_class = BakeryProductCategoryForm
    template_name = 'bakery/bakery_product/edit_category_form.html'  # Specify your template name

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(BakeryProductCategory, pk=pk)

    def form_valid(self, form):
        form.save()
        return redirect('bakery:category-list')  # Redirect to the category list after saving

#---------------------- Bakery Customer Opening Balance List View ------------------#

class BakeryCustomerOpeningBalanceListView(ListView):
    model = BakeryCustomerOpeningBalance
    template_name = 'bakery/customer_opening_balance/list.html'
    context_object_name = 'customer_opening_balances'


#---------------------- Bakery Customer Opening Balance Create View ------------------#

class BakeryCustomerOpeningBalanceCreateView(CreateView):
    model = BakeryCustomerOpeningBalance
    template_name = 'bakery/customer_opening_balance/add_edit.html'
    fields = ['date', 'invoice', 'customer', 'description', 'amount_owed']
    success_url = reverse_lazy('bakery:customer-opening-balance-list')

#---------------------- Bakery Customer Opening Balance Update View ------------------#
class BakeryCustomerOpeningBalanceUpdateView(UpdateView):
    model = BakeryCustomerOpeningBalance
    template_name = 'bakery/customer_opening_balance/add_edit.html'
    fields = ['date', 'invoice', 'customer', 'description', 'amount_owed']
    success_url = reverse_lazy('bakery:customer-opening-balance-list')

#--------------------- Returns View--------------------------#
class BakeryReturnsItemsListView(ListView):
    model = BakeryInvoice  # Change model to BakeryReturnsItems
    template_name = 'bakery/invoice/returns-list.html'
    context_object_name = 'return_items'  # Update context object name to match your template

    def get_queryset(self):
        # Start by filtering for return items with the status 'Return Inwards'
        return BakeryInvoice.objects.filter(status='Return Inwards')  # Assuming a foreign key to BakeryInvoice

    def get_context_data(self, **kwargs):
        # Get the existing context
        context = super().get_context_data(**kwargs)

        # Get start date and end date from the GET request
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        # Parse the dates and check if they are valid
        if start_date:
            start_date = parse_date(start_date)
        if end_date:
            end_date = parse_date(end_date)
        else:
            end_date = now().date()  # Default to today's date if end_date is not provided

        # Filter the queryset by date range if start_date is provided
        if start_date:
            context['return_items'] = context['return_items'].filter(created__range=[start_date, end_date])

        # Calculate the total amount for the filtered return items
        total_return_amount = context['return_items'].aggregate(total=Sum('invoice_total'))['total'] or 0  # Handle None value
        context['total_invoice_amount'] = total_return_amount
        context['start_date'] = start_date
        context['end_date'] = end_date

        return context

#class BakeryReturnsItemsListView(ListView):
    #model = BakeryReturnsItems
    #template_name = 'bakery/invoice/returns-list.html'
    #context_object_name = 'return_items'

    #def get_queryset(self):
        # Ensure that related `customer` objects are properly fetched
        #return super().get_queryset().select_related('customer')

# class BakeryReturnsItemsCreateView(CreateView):
#     model = BakeryReturnsItems
#     template_name = 'bakery/customer_return_items_form.html'
#     fields = ['date', 'customer', 'invoice', 'product', 'quantity', 'price', 'total']
#     success_url = reverse_lazy('bakery:customer-return-items-list')

#---------------------- Returns List Views ------------------#

class BakeryReturnsItemsUpdateView(UpdateView):
    model = BakeryReturnsItems
    template_name = 'bakery/invoice/edit-returns.html'
    fields = ['date', 'customer', 'invoice', 'product', 'quantity', 'price', 'total']
    success_url = reverse_lazy('bakery:customer-return-items-list')

#--------------------------------------------------------#

#---------------------- Bakery Sales Invoice View ------------------#
# Create your views here.
def invoice_view(request):
    invoices = BakeryInvoice.objects.filter(status='Sales')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        invoices = invoices.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('invoice_total')).values())[0]

    else:
        invoices = invoices
        total_invoice_amount = list(invoices.aggregate(Sum('invoice_total')).values())[0]

    template_name = 'bakery/invoice/invoices.html'
    context = {
                'invoices':invoices,
                'total_invoice_amount':total_invoice_amount,
                'status':0,
                }
    return render(request, template_name, context)



def returns_view(request):
    invoices = BakeryInvoice.objects.filter(status='Return Inwards')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        invoices = invoices.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('invoice_total')).values())[0]

    else:
        invoices = invoices
        total_invoice_amount = list(invoices.aggregate(Sum('invoice_total')).values())[0]

    template_name = 'bakery/invoice/invoices.html'
    context = {
                'invoices':invoices,
                'total_invoice_amount':total_invoice_amount,
                'status':1,
                }
    return render(request, template_name, context)


#---------------------- Bakery Sales Invoice Detail ------------------#
# Detail view of invoices
def invoice_detail(request, pk):

    invoice = BakeryInvoice.objects.get(id=pk)
    invoice_detail = BakeryInvoiceDetail.objects.filter(invoice=invoice)

    items = invoice.bakeryinvoicedetail_set.all()
    items_total = list(items.aggregate(Sum('total')).values())[0]

    invoice_payments = invoice.bakeryinvoicepayment_set.all()
    total_payments = list(invoice_payments.aggregate(Sum('amount_paid')).values())[0]
    payment_installment_count = invoice_payments.count()

    return_items = invoice.bakeryreturnsitems_set.all()
    total_returns = list(return_items.aggregate(Sum('total')).values())[0]
    

    print(invoice)

    context = {
        'invoice': invoice,
        "invoice_detail": invoice_detail,
        #'items_total':items_total,
        'invoice_payments':invoice_payments,
        'total_payments':total_payments,
        'payment_installment_count':payment_installment_count,

        "return_items":return_items,
        'total_returns':total_returns,

    }

    return render(request, "bakery/invoice/invoice-template.html", context)

#---------------------- Create Bakery Sales Invoice ------------------#
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta, date
def create_invoice(request):
    form = BakeryInvoiceForm()
    formset = BakeryInvoiceDetailFormSet()
    if request.method == "POST":
        
        # Extract the main form data from the POST request
        customer_id = request.POST.get("customer")
        created = request.POST.get("created")
        sales_session = request.POST.get("sales_session")
        sales_person = request.POST.get("sales_person")
        status = request.POST.get("status")

        # Print the extracted values
        print(f"customer_id: {customer_id}")
        print(f"created: {created}")
        print(f"sales_session: {sales_session}")
        print(f"sales_person: {sales_person}")
        print(f"status: {status}")
        

        # Fetch the customer instance
        customer = get_object_or_404(BakeryCustomer, pk=customer_id)

        # Print the customer instance to verify it's fetched correctly
        print(f"customer: {customer}")

        # Create the invoice object
        if sales_person and customer and created and sales_session:
            invoice = BakeryInvoice.objects.create(
                customer=customer,  # Assign the customer instance here
                created=created,
                sales_session=sales_session,
                sales_person=sales_person,
                status=status
            )
            print("Invoice created:", invoice)

            # Initialize total
            total = 0
            print("total gotten")
            # Process each row of invoice details
            row_count = int(request.POST.get("row_count", 0))  # Number of rows
            print("row gotten: ", row_count)
            for i in range(1, row_count + 1):
                print("in for loop")
                product_id = request.POST.get(f"product_{i}")
                quantity = Decimal(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                discount_price = float(request.POST.get(f"discount_price_{i}", 0))

                product = get_object_or_404(BakeryProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},Discount Price: {discount_price}")

                if  product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    # Create and save the BakeryInvoiceDetail
                    detail = BakeryInvoiceDetail.objects.create(
                        invoice=invoice,
                        product=product,
                        quantity=quantity,
                        price=price,
                        discount_price=discount_price,
                    )
                    print(f"Saved detail for row {i}:", detail)

            # Save the total invoice amount
            invoice.invoice_total = total
            invoice.save()
            print("Invoice total saved:", invoice.invoice_total)

            # Optionally, return a JSON response indicating success
            return JsonResponse({"success": True, "invoice_id": invoice.id})

        else:
            print("Error: Missing required invoice data")
            return JsonResponse({"success": False, "error": "Missing required invoice data"})

    # Handle GET requests or return an empty form for non-POST requests
    form = BakeryInvoiceForm()
    context = {
        "form": form,
        'formset': formset,
        }
    return render(request, "bakery/invoice/create_invoice.html", context)

#---------------------- Edit Bakery Sales Invoice ------------------#
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

def edit_invoice(request, pk):
    # Fetch the existing invoice using the provided primary key (pk)
    invoice = get_object_or_404(BakeryInvoice, id=pk)
    
    # Fetch the associated invoice details
    invoice_details = BakeryInvoiceDetail.objects.filter(invoice=invoice)
    
    if request.method == "POST":
        # Extract main form data from the POST request
        customer_id = request.POST.get("customer")
        created = request.POST.get("created")
        sales_session = request.POST.get("sales_session")
        sales_person = request.POST.get("sales_person")
        status = request.POST.get("status")

        # Fetch the customer instance
        customer = get_object_or_404(BakeryCustomer, pk=customer_id)

        # Update the invoice object
        if sales_person and customer and created and sales_session:
            invoice.customer = customer  # Update the customer instance
            invoice.created = created
            invoice.sales_session = sales_session
            invoice.sales_person = sales_person
            invoice.status = status
            invoice.save()
            print("Invoice updated:", invoice)

            # Initialize total
            total = 0
            # Process each row of invoice details
            row_count = int(request.POST.get("row_count", 0))  # Number of rows
            for i in range(1, row_count + 1):
                product_id = request.POST.get(f"product_{i}")
                quantity = Decimal(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                discount_price = float(request.POST.get(f"discount_price_{i}", 0))

                product = get_object_or_404(BakeryProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price}, Discount Price: {discount_price}")

                if product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount

                    # Update or create the corresponding BakeryInvoiceDetail
                    if i <= len(invoice_details):
                        detail = invoice_details[i-1]  # Update existing detail
                        detail.product = product
                        detail.quantity = quantity
                        detail.price = price
                        detail.discount_price = discount_price
                        detail.save()
                        print(f"Updated detail for row {i}: {detail}")
                    else:
                        # If there are fewer details than rows, create new ones
                        detail = BakeryInvoiceDetail.objects.create(
                            invoice=invoice,
                            product=product,
                            quantity=quantity,
                            price=price,
                            discount_price=discount_price,
                        )
                        print(f"Created new detail for row {i}: {detail}")

            # Save the total invoice amount
            invoice.invoice_total = total
            invoice.save()
            print("Invoice total saved:", invoice.invoice_total)

            # Optionally, return a JSON response indicating success
            return JsonResponse({"success": True, "invoice_id": invoice.id})

        else:
            print("Error: Missing required invoice data")
            return JsonResponse({"success": False, "error": "Missing required invoice data"})

    # Handle GET requests or return the form pre-filled with the existing invoice details
    form = BakeryInvoiceForm(instance=invoice)
    
    # Prepare the formset with the existing details
    formset_data = [{'product': detail.product.id, 'quantity': detail.quantity, 'price': detail.price, 'discount_price': detail.discount_price}
                    for detail in invoice_details]
    initial_data = [{'product': detail.product, 'quantity': detail.quantity, 'price': detail.price, 'discount_price': detail.discount_price}
                        for detail in invoice_details]
    BakeryInvoiceDetailFormSet = modelformset_factory(
    BakeryInvoiceDetail,
    form=BakeryInvoiceDetailForm,
    extra=0  # No extra forms, handled in the view or template
    )
    # You might need a custom formset initialization to handle editing the details
    formset = BakeryInvoiceDetailFormSet(queryset=invoice_details, initial=initial_data)
    print(type(invoice_details))  # Should be <class 'django.db.models.query.QuerySet'>

    context = {
        "form": form,
        'formset': formset,
        "invoice": invoice,  # Pass the invoice to the template if needed
    }
    return render(request, "bakery/invoice/edit_invoice.html", context)



#---------------------- Invoice Payment View  ------------------#
def InvoicePayment_view(request):
        invoice = BakeryInvoice.objects.all()
        customer = Customer.objects.all()
        invoice_payment = BakeryInvoicePayment.objects.all().order_by('-date')
        #invoice_grand_total = list(invoices.aggregate(Sum('grand_total')).values())[0]
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date:
            invoice_payment = invoice_payment.filter(created__range=[start_date, end_date])
        else:
            invoice_payment = BakeryInvoicePayment.objects.all().order_by('-date')
            #total_orders = list(invoices.aggregate(Sum('amount')).values())[0]
        #for payment in invoice_payment:
            #print("Invoice payment:", payment.invoice)
        template_name = 'bakery/invoice/invoice_payments.html'
        context = {
                    'invoice_payment':invoice_payment,
                    "invoice":invoice,
                    "customer":customer ,
                    
                    }
        return render(request, template_name, context)
    
#---------------------- Add Payment View ------------------#
class add_payment_view(SuccessMessageMixin, CreateView):
        model = BakeryInvoicePayment
        template_name = 'bakery/invoice/add_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("bakery:invoice-payments")
        success_message = 'Payment Transaction successful'

#---------------------- Payment Edit View ------------------#
class edit_payment_view(SuccessMessageMixin, UpdateView):
        model = BakeryInvoicePayment
        template_name = 'bakery/invoice/add_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("bakery:invoice-payments")
        success_message = 'Payment Transaction successfully Updated'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # context['payment_details']
            payment_details= get_object_or_404(BakeryInvoicePayment, pk=self.kwargs['pk'])
            context['payment_details'] = payment_details
            print("Payment details:", payment_details.pk)
            return context
        
#---------------------- Add Returns ------------------#
class add_returns_view(SuccessMessageMixin, CreateView):
        model = BakeryReturnsItems
        template_name = 'bakery/invoice/add_returns.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy('bakery:invoice-payments')
        success_message = 'Payment Transaction successful'
        
        
#---------------------- Payment Details ------------------#
from django.shortcuts import render, get_object_or_404
def payment_details_view(request, pk):
    # Get the payment detail object or return 404 if not found
    payment_detail = get_object_or_404(BakeryInvoicePayment, pk=pk)
    print("Payment details:", payment_detail)
    
    # Get the related invoice
    invoice = payment_detail.invoice  # Directly access the related invoice
    print("Invoice:", invoice)
    
    # Fetch all payment installments for the specific invoice
    invoice_payments = invoice.bakeryinvoicepayment_set.all()
    payment_installment_count = invoice_payments.count()
    
    # Pass the data to the template
    context = {
        'invoice': invoice,
        'payment_detail': payment_detail,
        'payment_installment_count': payment_installment_count,  # Add payment installment count to context
        'invoice_payments': invoice_payments,  # Optional: include all payment details for the invoice
    }
    print("Context:", context)
    
    return render(request, 'bakery/invoice/payment_details.html', context)

########################PURCHASES##############
# Create your views here.
@login_required
def purchases_view(request):
    purchases = BakeryPurchase.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    print(purchases)
    if start_date:
        purchases = purchases.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(purchases.filter(created__range=[start_date, end_date]).aggregate(Sum('purchase_total')).values())[0]

    else:
        purchases = purchases
        total_invoice_amount = list(purchases.aggregate(Sum('purchase_total')).values())[0]

    template_name = 'bakery/purchases/purchase_invoices.html'
    context = {
                'purchases':purchases,
                'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)
 
    #--------------------------------------------------------#
    # Detail view of invoices
@login_required
def purchase_detail(request, pk):
    # Fetch the specific BakeryPurchase instance using its primary key (pk)
    purchase = get_object_or_404(BakeryPurchase, id=pk)
    
    # Get all associated BakeryPurchaseSummary objects related to this purchase
    purchases_detail = BakeryPurchaseItems.objects.filter(purchase_id=purchase)
    
    # Fetch all payments related to this purchase
    purchase_invoice_payments = BakeryPurchasePayment.objects.filter(invoice=purchase.id)
    purchase_items = BakeryPurchaseItems.objects.filter(purchase_id=purchase.id)
    # Calculate the total amount paid so far
    total_payments = purchase_invoice_payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    
    # Calculate the total number of payment installments
    payment_installment_count = purchase_invoice_payments.count()
    supplier = purchase.supplier_name
    # Uncomment and modify the following lines if return items are needed
    # return_items = purchase.returnsitems_set.all()
    # total_returns = return_items.aggregate(Sum('total'))['total__sum'] or 0
    print(purchase.department)
    # Context to pass to the template
    context = {
        'purchase': purchase,
        'purchases_detail': purchases_detail,
        'purchase_invoice_payments': purchase_invoice_payments,
        'total_payments': total_payments,
        'payment_installment_count': payment_installment_count,
        'supplier': supplier,
        'purchase_items':purchase_items
        # Uncomment if handling returns
        # 'return_items': return_items,
        # 'total_returns': total_returns,
    }
    
    # Render the template with the context
    return render(request, "bakery/purchases/purchases-invoice-template.html", context)
#---------------------------------------------------------------------------------------#
# BakeryInvoice view
@login_required
def create_purchase(request):

    form = BakeryPurchaseForm()
    formset = BakeryPurchaseItemsFormSet(queryset=BakeryPurchase.objects.none())
    if request.method == "POST":
        
        supplier_id=int(request.POST.get("supplier_name"))
        created=request.POST.get("created")
        ordered_date_str = request.POST.get("ordered_date")
        received_date_str = request.POST.get("recieved_date")
        department = Department.objects.filter(department_name="Bakery").first()  # Set the department to "Bakery"
        employee = request.POST.get("employee")
        print(f"supplier_id (after conversion): {supplier_id}")
        # print(f"department (after conversion): {department}")
        supplier = get_object_or_404(BakerySupplier, pk=supplier_id)
        print(f"supplier_id: {supplier}")
        print(f"created: {created} ordered_date: {ordered_date_str} received_date: {received_date_str}")
        # print(f"department: {department}")
        print(f"employee: {employee}")
        print(f"supplier: {supplier} ")

        ordered_date_str = request.POST.get("ordered_date")
        received_date_str = request.POST.get("recieved_date")

        # Parse the date strings into datetime objects
        ordered_date = datetime.strptime(ordered_date_str, "%Y-%m-%dT%H:%M") if ordered_date_str else None
        received_date = datetime.strptime(received_date_str, "%Y-%m-%dT%H:%M") if received_date_str else None

        # Convert to timezone-aware datetime
        if ordered_date:
            ordered_date = timezone.make_aware(ordered_date)
        if received_date:
            received_date = timezone.make_aware(received_date)
            
        if supplier and employee and created:
            invoice = BakeryPurchase.objects.create(
                supplier_name=supplier,  # Assign the customer instance here
                created=created,
                ordered_date=ordered_date,
                recieved_date=received_date,
                # lead_time_days=lead_time_days,
                # department=department,
                employee=employee
            )
            print("Invoice created:", invoice)
            #-------------------- Invoice Created-------------------------#
            
            #-------------------- InvoiceItems Starts Here-------------------------#
            total = 0
            print("total gotten")
            
            # Process each row of invoice details
            row_count = int(request.POST.get("row_count", 0))  # Number of rows
            print("row gotten: ", row_count)
            for i in range(1, row_count + 1):
                print("in for loop")
                product_id = request.POST.get(f"raw_material{i}")
                quantity = Decimal(request.POST.get(f"quantity_{i}", 0))
                price = Decimal(request.POST.get(f"price_{i}", 0))
                discount_price = Decimal(request.POST.get(f"discount_amount_{i}", 0))

                product = get_object_or_404(RawMaterials, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},Discount amount: {discount_price}")

                if  product and quantity and price:
                    # Calculate the sum for each row
                    row_total = Decimal(price) * Decimal(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    # Create and save the BakeryInvoiceDetail
                    detail = BakeryPurchaseItems.objects.create(
                        purchase_id=invoice,
                        raw_material=product,
                        quantity=quantity,
                        price=price,
                        discount_amount=discount_price,
                        ordered_date=ordered_date,
                        recieved_date=received_date,
                    )
                    print(f"Saved detail for row {i}:", detail)

            # Save the total invoice amount
            invoice.purchase_total = total
            invoice.save()
            print("Invoice total saved:", invoice.purchase_total)

            # Optionally, return a JSON response indicating success
            return JsonResponse({"success": True, "invoice_id": invoice.id})

        else:
            print("Error: Missing required invoice data")
            return JsonResponse({"success": False, "error": "Missing required invoice data"})

        #return redirect("bakery:purchases")

    context = {

        #"total_invoice": total_invoice,
        "form": form,
        "formset": formset,
    }

    return render(request, "bakery/purchases/create_purchase.html", context)
#--------------------------------------------------------------------#

@login_required
def edit_purchase(request, pk):
    # Fetch the existing invoice and its items
    invoice = get_object_or_404(BakeryPurchase, pk=pk)
    invoice_items = BakeryPurchaseItems.objects.filter(purchase_id=invoice)
    BakeryPurchaseItemsFormSet = modelformset_factory(BakeryPurchaseItems, form=BakeryPurchaseItemsForm, extra=0, can_delete=True)

    # Initialize the forms with existing invoice data
    form = BakeryPurchaseForm(instance=invoice)
    formset = BakeryPurchaseItemsFormSet(queryset=invoice_items)

    if request.method == "POST":
        # Extract the main form data from the POST request
        supplier_id = int(request.POST.get("supplier_name"))
        created = request.POST.get("created")
        # ordered_date = timezone.make_aware(request.POST.get("ordered_date"))
        # recieved_date = timezone.make_aware(request.POST.get("recieved_date"))
        department = "Bakery"  # Set the department to 'Bakery'
        employee = request.POST.get("employee")
        
        ordered_date_str = request.POST.get("ordered_date")
        received_date_str = request.POST.get("recieved_date")

        # Parse the date strings into datetime objects
        ordered_date = datetime.strptime(ordered_date_str, "%Y-%m-%dT%H:%M") if ordered_date_str else None
        received_date = datetime.strptime(received_date_str, "%Y-%m-%dT%H:%M") if received_date_str else None

        # Convert to timezone-aware datetime
        if ordered_date:
            ordered_date = timezone.make_aware(ordered_date)
        if received_date:
            recieved_date = timezone.make_aware(received_date)
        
        print("department:", department)
        print("employee:", employee)
        print("supplier_id:", supplier_id)
        print("created:", created)
        print("ordered_date_str:", ordered_date_str)
        print("received_date_str:", received_date_str)
        print("ordered_date:", ordered_date)
        print("received_date:", received_date)
        print("ordered_date (aware):", ordered_date)
        print("recieved_date (aware):", recieved_date)

        # Fetch the supplier instance
        supplier = get_object_or_404(BakerySupplier, pk=supplier_id)

        # Ensure all necessary fields are provided
        if supplier and employee and created:
            # Update the invoice object
            invoice.supplier_name = supplier
            invoice.created = created
            invoice.ordered_date = ordered_date
            invoice.recieved_date = recieved_date
            invoice.department = department
            invoice.employee = employee
            invoice.save()
            print("Invoice updated:", invoice)

            # Initialize the total
            total = 0

            # Process each row of invoice details
            row_count = int(request.POST.get("row_count", 0))  # Number of rows
            print("row gotten: ", row_count)
            for i in range(1, row_count + 1):
                # Get existing invoice item or set to None if not available
                detail = invoice_items[i-1].id if i <= len(invoice_items) else None

                # Retrieve form data for the current row
                product_id = request.POST.get(f"raw_material{i}")
                quantity = Decimal(request.POST.get(f"quantity_{i}", 0))
                price = Decimal(request.POST.get(f"price_{i}", 0))
                discount_price = Decimal(request.POST.get(f"discount_amount_{i}", 0))

                # Fetch the product instance
                product = get_object_or_404(RawMaterials, pk=product_id)
                
                if product and quantity and price:
                    # Calculate the sum for each row
                    row_total = Decimal(price) * Decimal(quantity)
                    total += row_total  # Add to the total invoice amount
                    # print(f"Row {i} total: {row_total}, Cumulative total: {total}")
                    print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},Discount amount: {discount_price}")
                    if i <= len(invoice_items):
                        # Update existing detail
                        detail = invoice_items[i-1]
                        detail.raw_material = product
                        detail.quantity = quantity
                        detail.price = price
                        detail.discount_amount = discount_price
                        detail.ordered_date = ordered_date
                        detail.recieved_date = recieved_date
                        detail.save()
                        print(f"Updated detail for row {i}: {detail}")
                    else:
                        # If there are fewer details than rows, create new ones
                        detail = BakeryPurchaseItems.objects.create(
                            purchase_id=invoice,
                            raw_material=product,
                            quantity=quantity,
                            price=price,
                            discount_amount=discount_price,
                            ordered_date=ordered_date,
                            recieved_date=recieved_date,
                        )
                        print(f"Created new detail for row {i}: {detail}")

            # Save the updated total invoice amount
            invoice.purchase_total = total
            invoice.save()
            print("Invoice total updated:", invoice.purchase_total)

            # Optionally, return a JSON response indicating success
            return JsonResponse({"success": True, "invoice_id": invoice.id})

        else:
            print("Error: Missing required invoice data")
            return JsonResponse({"success": False, "error": "Missing required invoice data"})

    context = {
        "form": form,
        "formset": formset,
        "invoice": invoice,
    }

    return render(request, "bakery/purchases/create_purchase.html", context)


# BakeryInvoice view
@login_required
def purchase_invoice_payments_view(request):
        invoice = BakeryInvoice.objects.all()
        supplier = BakerySupplier.objects.all()
        purchase_invoice_payment = BakeryPurchasePayment.objects.all().order_by('-date')
        #invoice_grand_total = list(invoices.aggregate(Sum('grand_total')).values())[0]

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date:
            purchase_invoice_payment = purchase_invoice_payment.filter(created__range=[start_date, end_date])
            #total_orders = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('amount')).values())[0]

        else:
            purchase_invoice_payment = purchase_invoice_payment
            #total_orders = list(invoices.aggregate(Sum('amount')).values())[0]

        template_name = 'bakery/purchases/purchase_invoice_payments.html'
        context = {
                    'purchase_invoice_payment':purchase_invoice_payment,
                    "invoice":invoice,
                    "supplier":supplier ,

                    }
        return render(request, template_name, context)
    
class add_purchase_payment_view(SuccessMessageMixin, CreateView):
        model = BakeryPurchasePayment
        template_name = 'bakery/purchases/add_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("bakery:purchases")
        success_message = 'Payment Transaction successful'

# BakeryInvoice view
class edit_purchase_payment_view(SuccessMessageMixin, UpdateView):
        model = BakeryPurchasePayment
        template_name = 'bakery/purchases/edit_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("bakery:purchases")
        success_message = 'Payment Transaction successfully Updated'







###################################SUPPLIER############################

# Create your views here.
@login_required
def suppliers_view(request):
    suppliers = BakerySupplier.objects.all()

    template_name = 'bakery/supplier/suppliers.html'
    context = {'suppliers':suppliers}
    return render(request, template_name, context)
#-------------------------------------------------------------------#
@login_required
def supplier_details(request, id):#
    supplier = get_object_or_404(BakerySupplier, id=id)

    supplier_invoice = supplier.bakerypurchase_set.all()
    supplier_invoice_total = list(supplier_invoice.aggregate(Sum('purchase_total')).values())[0]

    # opening_balance = supplier.bakerycustomeropeningbalance_set.all()
    
    # returns = supplier.bakeryreturnsitems_set.all()
    # returns_total = list(returns.aggregate(Sum('total')).values())[0]


    # purchase_payments = supplier.bakerypurchasepayment_set.all()
    # total_purchase_payment= list(purchase_payments.aggregate(Sum('purchase_total')).values())[0]
    # print(purchase_payments)
    template_name = 'bakery/supplier/supplier_account.html'
    context = {'supplier':supplier,
                # 'opening_balance':opening_balance,
                'supplier_invoice':supplier_invoice,
                'supplier_invoice_total':supplier_invoice_total,
                # 'returns':returns,
                # 'returns_total':returns_total,
                # 'purchase_payments':purchase_payments,
                # 'total_purchase_payment':total_purchase_payment,
                }
 
    return render(request, template_name, context)
#-------------------------------------------------------------------------#
class add_supplier(SuccessMessageMixin, CreateView):
    model = BakerySupplier
    template_name = 'bakery/supplier/forms/add_supplier.html'
    fields = '__all__'
    exclude = ('slug',)
    success_url = reverse_lazy('bakery:supplier')
    success_message = 'supplier Account Successfully Created !!!'

#-------------------------------------------------------------------------#
class edit_supplier(SuccessMessageMixin, UpdateView):
    model = BakerySupplier
    template_name = 'bakery/supplier/forms/edit_supplier.html'
    fields = '__all__'
    exclude = ('slug',)
    success_url = reverse_lazy('bakery:supplier')
    success_message = 'supplier Account Successfully Edited !!!'
#-------------------------------------------------------------------------#


#--------------------------- Production --------------------------------#

#----- Production List -------#
from django.core.cache import cache

class BakeryProductionListView(ListView):
    model = BakeryProduction
    template_name = 'bakery/production/production_list.html'
    context_object_name = 'productions'


from django.db.models import Sum

def bakery_production_list(request):
    # if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     return JsonResponse({'success': False, 'error': 'Invalid request type'}, status=400)

    queryset = None
    if queryset is None:
        queryset = BakeryProduction.objects.all()

        # Filter logic based on form inputs
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        production_id = request.GET.get('production_id')
        supervisor = request.GET.get('supervisor')
        stock_supervisor = request.GET.get('stock_supervisor')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
            print("Filtered by start_date:", start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
            print("Filtered by end_date:", end_date)
        if production_id:
            queryset = queryset.filter(production_id__icontains=production_id)
            print("Filtered by production_id:", production_id)
        if supervisor:
            queryset = queryset.filter(supervisor__icontains=supervisor)
            print("Filtered by supervisor:", supervisor)
        if stock_supervisor:
            queryset = queryset.filter(stock_supervisor__icontains=stock_supervisor)
            print("Filtered by stock_supervisor:", stock_supervisor)

        # cache.set('production_queryset', queryset, 60)
        # print("Cached queryset:", queryset)

    productions = list(queryset.values(
        'id',
        'created_at',
        'department',
        'production_id',
        'sub_department__sub_department_name',
        'session',
        'supervisor',
        'stock_supervisor'
    ))
    # print("Productions:", productions)

    raw_material_usages = BakeryRawMaterialUsage.objects.filter(
        production_id__in=queryset
    ).values(
        'production_id__production_id',
        'production_id__created_at',
        'production_id__supervisor',
        'production_id__sub_department__sub_department_name',
        'raw_material__raw_material_name',
        'status',
        'qty',
        'unit_cost_price',
        'raw_material_value'
    )
    # print("Raw Material Usages:", list(raw_material_usages))

    total_raw_material_val = raw_material_usages.aggregate(
        total_value=Sum('raw_material_value')
    )['total_value'] or 0
    # print("Total Raw Material Value:", total_raw_material_val)

    outputs = BakeryProductionOutput.objects.filter(
        production_id__in=queryset
    ).values(
        'production_id__production_id',
        'production_id__created_at',
        'production_id__supervisor',
        'production_id__sub_department__sub_department_name',
        'output_category',
        'product__product_name',
        'mixture_number',
        'qty',
        'product_price',
        'value'
    )
    # print("Outputs:", list(outputs))

    total_output_value = outputs.aggregate(
        total_value=Sum('value')
    )['total_value'] or 0
    # print("Total Output Value:", total_output_value)
    return JsonResponse({
        'success': True,
        'productions': productions,
        'raw_material_usages': list(raw_material_usages),
        'outputs': list(outputs),
        'total_raw_material_val': total_raw_material_val,
        'total_output_value': total_output_value,
        'start_date':start_date,
        'end_date':end_date,
        'production_id':production_id,
        'supervisor':supervisor,
        'stock_supervisor':stock_supervisor

    })


    
    
#----- Production Details -------#
def production_detail(request, pk):

    production = BakeryProduction.objects.get(id=pk)
    output = BakeryProductionOutput.objects.filter(production_id=production)
    raw_material = BakeryRawMaterialUsage.objects.filter(production_id=production)
    total_raw_material_value = sum([rm.raw_material_value for rm in raw_material])

    total_output_value = sum([o.value for o in output])
    gross_profit = total_output_value - total_raw_material_value
    print(output)

    context = {
        'invoice': production,
        "output": output,
        'raw_material':raw_material,
        'total_raw_material_value': total_raw_material_value,
        'total_output_value':total_output_value,
        'gross_profit':gross_profit
    }
# return render(request, 'your_template.html', {'total_raw_material_value': total_raw_material_value})
    return render(request, "bakery/production/production_detail.html", context)    
    
#----- Create Production -------#
def create_production(request):
    # Initialize the form for the main BakeryProduction details
    form = BakeryProductionForm()
    # Initialize the formset for handling multiple raw material usages
    formset = BakeryRawMaterialUsageFormSet(queryset=BakeryProduction.objects.none())
    formset2 = BakeryProductionOutputFormset(queryset=BakeryProductionOutput.objects.none())

    # Check if the request is a POST request (form submission)
    if request.method == "POST":
        # Extract individual fields from the POST request data
        created_at = request.POST.get("created_at")
        mixture_number = request.POST.get("mixture_number")
        department = "Bakery"
        sub_department_id = request.POST.get("sub_department")
        session = request.POST.get("session")
        supervisor = request.POST.get("supervisor")
        stock_supervisor = request.POST.get("stock_supervisor")

        # Print the values
        print("Created At:", created_at)
        print("Mixture Number:", mixture_number)
        print("Department:", department)
        print("Sub Department ID:", sub_department_id)
        print("Session:", session)
        print("Supervisor:", supervisor)
        print("Stock Supervisor:", stock_supervisor)

        # Fetch the SubDepartment instance based on the provided ID
        sub_department = get_object_or_404(SubDepartment, pk=sub_department_id)
        print("Sub Department:", sub_department)

        # Check if all the required fields are present before creating a BakeryProduction object
        if created_at and mixture_number and department and sub_department and session and supervisor and stock_supervisor:
            # Create a new BakeryProduction object with the provided data
            production = BakeryProduction.objects.create(
                created_at=created_at,
                mixture_number=mixture_number,
                department=department,
                sub_department=sub_department,
                session=session,
                supervisor=supervisor,
                stock_supervisor=stock_supervisor
            )
            print("Production created:", production)  # Debugging statement to confirm creation
            
            # Initialize the total raw material usage cost to 0
            total = 0
            print("total gotten")  # Debugging statement to confirm total initialization
            
            # Get the total number of rows of raw material data from the POST request
            row_count = int(request.POST.get("row_count", 0))
            print("row gotten: ", row_count)  # Debugging statement to confirm row count retrieval
            
            # Loop through each row of raw material data submitted
            for i in range(1, row_count + 1):
                print("in for loop")  # Debugging statement to confirm entering the loop
                
                # Extract the product ID, quantity, and price from the POST data for each row
                product_id = request.POST.get(f"product_{i}")
                quantity = Decimal(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                status=request.POST.get(f"status_{i}")
                print(f"Product ID {i}:", product_id)
                print(f"Quantity {i}:", quantity)
                print(f"Price from form {i}:", price)
                # Fetch the RawMaterials instance using the extracted product ID
                product_price = BakeryPurchaseItems.objects.filter(raw_material=product_id).order_by('created').last()
                price= product_price.price
                print(f"Price from view {i}:", price)
                product = get_object_or_404(RawMaterials, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}")  # Debugging statement

                # Ensure all necessary data for the current row is present
                if product and quantity and price:
                    # Calculate the total cost for the current row
                    row_total = quantity * price
                    # Add the row total to the cumulative total cost
                    total += row_total
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")  # Debugging statement

                    # Create and save a BakeryPurchaseItems object for this row
                    detail = BakeryRawMaterialUsage.objects.create(
                        production_id=production,  # Associate the item with the created production
                        raw_material=product,
                        qty=quantity,
                        unit_cost_price=price,
                        status=status
                    )
                    print(f"Saved detail for row {i}:", detail)  # Debugging statement

            # Optionally, save the total raw material usage cost back to the production object
            production.total = total
            production.save()
            print("Production total saved:", production.total)  # Debugging statement

            # Return a JSON response indicating success and include the production ID
            return JsonResponse({"success": True, "production_id": production.production_id})

        else:
            # If any required data is missing, print an error and return a JSON response indicating failure
            print("Error: Missing required production data")
            return JsonResponse({"success": False, "error": "Missing required production data"})

    # If the request method is not POST, prepare the context with the empty form and formset for rendering the template
    context = {
        "form": form,
        "formset": formset,
        "formset2": formset2,
    }
    # Render the template for creating a production, passing in the form and formset
    return render(request, "bakery/production/create_production.html", context)


def edit_production(request, pk):
    # Fetch the BakeryProduction instance by its ID
    production = get_object_or_404(BakeryProduction, pk=pk)
    
    # Initialize the form for the BakeryProduction details with the existing instance
    form = BakeryProductionForm(instance=production)
    
    # Initialize formsets for handling the related raw material usage and output, with existing data
    BakeryRawMaterialUsageFormSet = modelformset_factory(BakeryRawMaterialUsage, form=BakeryRawMaterialUsageForm, extra=0, can_delete=True)
    formset = BakeryRawMaterialUsageFormSet(queryset=BakeryRawMaterialUsage.objects.filter(production_id=production))
    BakeryProductionOutputFormset = modelformset_factory(BakeryProductionOutput, form=BakeryProductionOutputForm, extra=0, can_delete=True)
    formset2 = BakeryProductionOutputFormset(queryset=BakeryProductionOutput.objects.filter(production_id=production))

    # Check if the request is a POST request (form submission)
    if request.method == "POST":
        # Extract individual fields from the POST request data
        created_at = request.POST.get("created_at")
        mixture_number = request.POST.get("mixture_number")
        department = "Bakery"
        sub_department_id = request.POST.get("sub_department")
        session = request.POST.get("session")
        supervisor = request.POST.get("supervisor")
        stock_supervisor = request.POST.get("stock_supervisor")

        # Print the values (for debugging)
        print("Created At:", created_at)
        print("Mixture Number:", mixture_number)
        print("Department:", department)
        print("Sub Department ID:", sub_department_id)
        print("Session:", session)
        print("Supervisor:", supervisor)
        print("Stock Supervisor:", stock_supervisor)

        # Fetch the SubDepartment instance based on the provided ID
        sub_department = get_object_or_404(SubDepartment, pk=sub_department_id)

        # Check if all the required fields are present
        if created_at and mixture_number and department and sub_department and session and supervisor and stock_supervisor:
            # Update the existing BakeryProduction object with the new data
            production.created_at = created_at
            production.mixture_number = mixture_number
            production.department = department
            production.sub_department = sub_department
            production.session = session
            production.supervisor = supervisor
            production.stock_supervisor = stock_supervisor
            production.save()

            # Initialize the total raw material usage cost to 0
            total = 0
            row_count = int(request.POST.get("row_count", 0))

            # Delete previous raw material usage entries
            BakeryRawMaterialUsage.objects.filter(production_id=production).delete()

            # Loop through each row of raw material data submitted
            for i in range(1, row_count + 1):
                product_id = request.POST.get(f"product_{i}")
                quantity = Decimal(request.POST.get(f"quantity_{i}", 0))
                price = Decimal(request.POST.get(f"price_{i}", 0))
                status = request.POST.get(f"status_{i}")

                product_price = BakeryPurchaseItems.objects.filter(raw_material=product_id).order_by('created').last()
                price = Decimal(product_price.price)

                product = get_object_or_404(RawMaterials, pk=product_id)

                if product and quantity and price:
                    row_total = Decimal(quantity) * Decimal(price)
                    total += row_total

                    # Create a new BakeryRawMaterialUsage object for this row
                    detail = BakeryRawMaterialUsage.objects.create(
                        production_id=production,
                        raw_material=product,
                        qty=quantity,
                        unit_cost_price=price,
                        status=status
                    )

            # Update the production's total cost
            production.total = total
            production.save()

            # Return a JSON response indicating success
            return JsonResponse({"success": True, "production_id": production.production_id})

        else:
            # If required data is missing, return an error response
            print("Error: Missing required production data")
            return JsonResponse({"success": False, "error": "Missing required production data"})

    # Prepare the context with the form and formsets pre-filled with the existing production data
    context = {
        "form": form,
        "formset": formset,
        "formset2": formset2,
        "production": production,
    }
    return render(request, "bakery/production/create_production.html", context)



#----- Create Production -------#
def create_production_out(request):
    # Initialize the form for the main BakeryProduction details
    if request.method == "POST":
        # Extract individual fields from the POST request data
        created_at = request.POST.get("created_at")
        mixture_number = request.POST.get("mixture_number")
        department = "Bakery"
        sub_department_id = request.POST.get("sub_department")
        session = request.POST.get("session")
        supervisor = request.POST.get("supervisor")
        stock_supervisor = request.POST.get("stock_supervisor")
        production_id = request.POST.get("production_id")
        # Print the values
        print("Created At:", created_at)
        print("Mixture Number:", mixture_number)
        print("Department:", department)
        print("Sub Department ID:", sub_department_id)
        print("Session:", session)
        print("Supervisor:", supervisor)
        print("Stock Supervisor:", stock_supervisor)

        # Fetch the SubDepartment instance based on the provided ID
        sub_department = get_object_or_404(SubDepartment, pk=sub_department_id)
        print("Sub Department:", sub_department)
        if production_id is not None and len(str(production_id)) < 10:
        # Check if all the required fields are present before creating a BakeryProduction object
            if created_at and mixture_number and department and sub_department and session and supervisor and stock_supervisor:
                # Create a new BakeryProduction object with the provided data
                production = BakeryProduction.objects.create(
                    created_at=created_at,
                    mixture_number=mixture_number,
                    department=department,
                    sub_department=sub_department,
                    session=session,
                    supervisor=supervisor,
                    stock_supervisor=stock_supervisor
                )
                print("Production created:", production)  # Debugging statement to confirm creation
            else:
            # If any required data is missing, print an error and return a JSON response indicating failure
                print("Error: Missing required production data")
                return JsonResponse({"success": False, "error": "Missing required production data"})

        else:    
            # Initialize the total raw material usage cost to 0
            print("Production Inherited:", production_id)
            production_id = get_object_or_404(BakeryProduction, production_id=production_id)
            total = production_id.total
            print("total gotten")  # Debugging statement to confirm total initialization
            
            # Get the total number of rows of raw material data from the POST request
            row_count = int(request.POST.get("row_count", 0))
            print("row gotten: ", row_count)  # Debugging statement to confirm row count retrieval
            
            # Loop through each row of raw material data submitted
            try:
                for i in range(1, row_count + 1):
                    print("in for loop")  # Debugging statement to confirm entering the loop
                    
                    # Extract the product ID, quantity, and price from the POST data for each row
                    output_category= request.POST.get(f"output_category_{i}")
                    product_id = request.POST.get(f"product_{i}")
                    quantity = Decimal(request.POST.get(f"quantity_{i}", 0))
                    tag = request.POST.get(f"tag_{i}")

                    # Fetch the RawMaterials instance using the extracted product ID
                    product = get_object_or_404(BakeryProduct, pk=product_id)
                    price=product.price
                    print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price}, Tag: {tag}")  # Debugging statement

                    # Ensure all necessary data for the current row is present
                    if product and quantity and price:
                        # Calculate the total cost for the current row
                        row_total = quantity * price
                        # Add the row total to the cumulative total cost
                        total += row_total
                        print(f"Row {i} total: {row_total}, Cumulative total: {total}")  # Debugging statement

                        # Create and save a BakeryPurchaseItems object for this row
                        detail = BakeryProductionOutput.objects.create(
                            output_category=output_category,
                            production_id=production_id,  # Associate the item with the created production
                            mixture_number=mixture_number,
                            product=product,
                            qty=quantity,
                            product_price=price,
                            tag =tag,
                            value=total
                        )
                        print(f"Saved detail for row {i}:", detail)  # Debugging statement
                    else:
                        # If any required data is missing, print an error and return a JSON response indicating failure
                        print("Error: Missing required production data")
                        return JsonResponse({"success": False, "error": "Missing required production data"})
            except Exception as e:
                print("Error:", e)
                return JsonResponse({"success": False, "error": "Error: Missing required production data"})

            # Optionally, save the total raw material usage cost back to the production object
            production_id.total = total
            production_id.save()
            print("Production total saved:", production_id.total)  # Debugging statement

            # Return a JSON response indicating success and include the production ID
            return JsonResponse({"success": True})

def edit_production_out(request, pk):
    # Fetch the BakeryProduction instance by its ID
    production = get_object_or_404(BakeryProduction, pk=pk)
    
    # Check if the request is a POST request (form submission)
    if request.method == "POST":
        # Extract individual fields from the POST request data
        created_at = request.POST.get("created_at")
        mixture_number = request.POST.get("mixture_number")
        department = "Bakery"
        sub_department_id = request.POST.get("sub_department")
        session = request.POST.get("session")
        supervisor = request.POST.get("supervisor")
        stock_supervisor = request.POST.get("stock_supervisor")

        # Print the values for debugging
        print("Created At:", created_at)
        print("Mixture Number:", mixture_number)
        print("Department:", department)
        print("Sub Department ID:", sub_department_id)
        print("Session:", session)
        print("Supervisor:", supervisor)
        print("Stock Supervisor:", stock_supervisor)

        # Fetch the SubDepartment instance based on the provided ID
        sub_department = get_object_or_404(SubDepartment, pk=sub_department_id)
        
        # Update the existing BakeryProduction object with the provided data
        if created_at and mixture_number and department and sub_department and session and supervisor and stock_supervisor:
            production.created_at = created_at
            production.mixture_number = mixture_number
            production.department = department
            production.sub_department = sub_department
            production.session = session
            production.supervisor = supervisor
            production.stock_supervisor = stock_supervisor
            production.save()
            print("Production updated:", production)  # Debugging statement

        else:
            # If any required data is missing, return an error response
            print("Error: Missing required production data")
            return JsonResponse({"success": False, "error": "Missing required production data"})

        # Initialize the total raw material usage cost to the existing value
        total = production.total
        print("Total before edit:", total)  # Debugging statement

        # Get the total number of rows of raw material data from the POST request
        row_count = int(request.POST.get("row_count", 0))
        print("Row count:", row_count)  # Debugging statement

        # Delete previous BakeryProductionOutput entries for the production to avoid duplicates
        BakeryProductionOutput.objects.filter(production_id=production).delete()

        # Loop through each row of output data submitted
        try:
            for i in range(1, row_count + 1):
                output_category = request.POST.get(f"output_category_{i}")
                product_id = request.POST.get(f"product_{i}")
                quantity = Decimal(request.POST.get(f"quantity_{i}", 0))
                status = request.POST.get(f"status_{i}", 0)
                tag = request.POST.get(f"tag_{i}")
                
                # Fetch the BakeryProduct instance using the extracted product ID
                product = get_object_or_404(BakeryProduct, pk=product_id)
                price = product.price
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},Status: {status}, Tag: {tag}")  # Debugging statement

                # Ensure all necessary data for the current row is present
                if product and quantity and price:
                    # Calculate the total cost for the current row
                    row_total = quantity * price
                    total += row_total
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")  # Debugging statement

                    # Create and save a BakeryProductionOutput object for this row
                    detail = BakeryProductionOutput.objects.create(
                        output_category=output_category,
                        production_id=production,
                        mixture_number=mixture_number,
                        product=product,
                        qty=quantity,
                        product_price=price,
                        value=row_total,
                        tag=tag
                        
                    )
                    print(f"Saved detail for row {i}:", detail)  # Debugging statement

                else:
                    # If any required data is missing, return an error response
                    print("Error: Missing required output data for row", i)
                    return JsonResponse({"success": False, "error": f"Missing required output data for row {i}"})
        
        except Exception as e:
            print("Error:", e)
            return JsonResponse({"success": False, "error": "Error: Missing required output data"})

        # Update and save the total output cost to the production object
        production.total = total
        production.save()
        print("Production total updated:", production.total)  # Debugging statement

        # Return a JSON response indicating success
        return JsonResponse({"success": True})

    # If the request method is not POST, just return an error since the edit logic should only handle POST requests
    return JsonResponse({"success": False, "error": "Invalid request method"})



def add_more_row_production(request):
    # Initialize a formset for additional rows, with a prefix to differentiate them
    formset = BakeryRawMaterialUsageFormSet(prefix='form')
    # Get an empty form from the formset to be rendered as a new row
    empty_form = formset.empty_form
    # Render the empty form to a string using a specific template for adding a new row
    rendered_row = render_to_string('bakery/production/new_row_production.html', {'form': empty_form})
    # Return a JSON response containing the HTML of the new row to be added dynamically in the frontend
    return JsonResponse({'row_html': rendered_row})

#--------------------------- / Production --------------------------------#


#--------------------------------------------------------#
# Detail view of inventories

@login_required
def inventory_view(request):
    inventory = BakeryInventory.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    #if start_date:
        #inventory = inventory.filter(created__range=[start_date, end_date])
        #total_invoice_amount = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('invoice_total')).values())[0]

    #else:
        #inventory = inventory
        #total_invoice_amount = list(invoices.aggregate(Sum('invoice_total')).values())[0]

    template_name = 'bakery/inventory/inventory.html'
    context = {
                'inventory':inventory,
                #'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)

class BakeryInventoryDetailView(DetailView):
    model = BakeryInventory
    template_name = 'bakery/inventory/inventory-detail-template.html'  # Customize this to your actual template path
    context_object_name = 'inventory'  # The context variable name for the object in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch related inventory items and add them to the context
        context['inventory_items'] = BakeryInventoryItems.objects.filter(inventory_id=self.object)
        return context


#--------------------------------------------------------#
def create_inventory(request):
    form = BakeryInventoryForm()
    formset = BakeryInventoryItemsFormSet(queryset=BakeryInventoryItems.objects.none())
    department=Department.objects.filter(department_name='Bakery').first()
    print(f"department: {department}")
    if request.method == "POST":
        # Extract the main form data from the POST request
        employee = request.POST.get("employee")
        created = request.POST.get("created")
        

        # Print the extracted values
        print(f"employee: {employee}")
        print(f"created: {created}")
      

        # Fetch the customer instance
        #customer = get_object_or_404(BakeryCustomer, pk=customer_id)

        # Print the customer instance to verify it's fetched correctly
        
        department=Department.objects.filter(department_name='Bakery').first()
        print(f"department: {department}")
        # Create the invoice object
        if employee and created:
            invoice = BakeryInventory.objects.create(
                created=created,  # Assign the customer instance here
                employee=employee,
                department_name=department,
            )
            print("Invoice created:", invoice)

            # Initialize total
            total = 0
            print("total gotten")
            # Process each row of invoice details
            row_count = int(request.POST.get("row_count", 0))  # Number of rows
            print("row gotten: ", row_count)
            for i in range(1, row_count + 1):
                print("in for loop")
                product_id = request.POST.get(f"product_{i}")
                print("p id",product_id)
                quantity = Decimal(request.POST.get(f"quantity_{i}", 0))
                price = Decimal(request.POST.get(f"price_{i}", 0))
                status = request.POST.get(f"status_{i}", 0)
                
                product = get_object_or_404(RawMaterials, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},status: {status}")

                if  product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    # Create and save the BakeryInvoiceDetail
                    detail = BakeryInventoryItems.objects.create(
                        inventory_id=invoice,
                        raw_material_name=product,
                        quantity=quantity,
                        price=price,
                        status=status,
                    )
                    print(f"Saved detail for row {i}:", detail)

            # Save the total invoice amount
            invoice.total_cost = total
            invoice.save()
            print("Invoice total saved:", invoice.total_cost)

            # Optionally, return a JSON response indicating success
            return JsonResponse({"success": True, "invoice_id": invoice.id})

        else:
            print("Error: Missing required invoice data")
            return JsonResponse({"success": False, "error": "Missing required invoice data"})

    # Handle GET requests or return an empty form for non-POST requests
    context = {
        "form": form,
        'formset': formset,
        }
    return render(request, "bakery/inventory/create_inventory.html", context)

@login_required
def edit_inventory(request, pk):
    # Fetch the existing inventory and its items
    invoice = get_object_or_404(BakeryInventory, pk=pk)
    invoice_items = BakeryInventoryItems.objects.filter(inventory_id=invoice)
    BarInventoryItemsFormSet = modelformset_factory(BakeryInventoryItems, form=BakeryInventoryItemsForm, extra=0, can_delete=True)

    # Initialize the forms with existing inventory data
    form = BakeryInventoryForm(instance=invoice)
    formset = BarInventoryItemsFormSet(queryset=invoice_items)

    if request.method == "POST":
        # Extract the main form data from the POST request
        employee = request.POST.get("employee")
        created = request.POST.get("created")
        department=Department.objects.filter(department_name="Bakery").first()
        print(f"department: {department}")
        # description = request.POST.get("description")
        # Update the inventory object
        if employee and created:
            invoice.employee = employee
            invoice.created = created
            invoice.department_name = department
            invoice.save()
            print("Invoice updated:", invoice)

            # Initialize total
            total = 0
            print("total gotten")

            # Process each row of inventory details
            row_count = int(request.POST.get("row_count", 0))  # Number of rows
            for i in range(1, row_count + 1):
                print("in for loop")
                product_id = request.POST.get(f"product_{i}")
                quantity = Decimal(request.POST.get(f"quantity_{i}", 0))
                price = Decimal(request.POST.get(f"price_{i}", 0))
                status = request.POST.get(f"status_{i}", 0)

                product = get_object_or_404(RawMaterials, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price}, Status: {status}")

                if product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    if i <= len(invoice_items):
                        # Update existing detail
                        detail = invoice_items[i - 1]
                        raw_material_name=product,
                        quantity=quantity,
                        price=price,
                        status=status,
                        detail.save()
                        print(f"Updated detail for row {i}: {detail}")
                    else:
                        # Create new detail if there are more rows than existing items
                        detail = BakeryInventoryItems.objects.create(
                            inventory_id=invoice,
                            raw_material_name=product,
                            quantity=quantity,
                            price=price,
                            status=status,
                        )
                        print(f"Created new detail for row {i}: {detail}")

            # Save the updated total invoice amount
            invoice.total_price = total
            invoice.save()
            print("Invoice total updated:", invoice.total_price)

            # Optionally, return a JSON response indicating success
            return JsonResponse({"success": True, "invoice_id": invoice.id})

        else:
            print("Error: Missing required invoice data")
            return JsonResponse({"success": False, "error": "Missing required invoice data"})

    context = {
        "form": form,
        "formset": formset,
        "invoice": invoice,
    }

    return render(request, "bakery/inventory/create_inventory.html", context)

def recipe(request):
    recipe=Recipe.objects.all()
    form=RecipeRawMaterialForm()
    formset=RecipeRawMaterialFormSet()

    context={
        'recipe':recipe,
        'formset':formset,
        'form':form
    }
    return render(request,'bakery/reciperawmaterials/recipe.html',context)





def convert_to_grams(quantity, measure):
    measure = measure.lower()  # Normalize measure to lower case
    if measure == 'kg':
        return quantity * 1000  # Convert kilograms to grams
    elif measure == 'litre':
        return quantity * 1000  # Approximate 1 liter to 1000 grams
    elif measure == 'unit' or measure == 'units':
        return quantity * 50  # 1 tray ≈ 30 eggs, 50g each
    elif measure == 'oil':
        return quantity * 920  # 1 liter of oil ≈ 920 grams
    elif measure == 'grams':
        return quantity  # Already in grams
    else:
        return quantity  # No conversion needed for unknown measures


def convert_to_label(quantity, measure,name):
    measure = measure.lower()  # Normalize measure to lower case
    if measure == 'kg':
        print(measure)
        return (quantity/1000)  # Convert grams to kilograms
    elif measure == 'litre':
        print(measure)
        return quantity/1000   # Approximate 1 liter to 1000 grams
    elif measure == 'unit' and name.lower() =='egg':
        print(measure)
        return (quantity/50 )  # 1 tray ≈ 30 eggs, 50g each
        #return quantity * 30 * 50  # 1 tray ≈ 30 eggs, 50g each
    elif measure == 'oil':
        print(measure)
        return quantity # 1 liter of oil ≈ 920 grams
    elif measure == 'grams':
        print(measure)
        return (quantity)  # Already in grams
    else:
        print(measure)
        return quantity  
def name(measure):
    measure = measure.lower()  # Normalize measure to lower case
    if measure == 'kg':
        #print(measure)
        return 'kg' #(quantity/1000)  # Convert grams to kilograms
    elif measure == 'litre':
        #print(measure)
        return 'L' #quantity   # Approximate 1 liter to 1000 grams
    elif measure == 'unit':# and name.lower() =='egg':
        #print(measure)
        return 'units' #(quantity/50 )  # 1 tray ≈ 30 eggs, 50g each
        #return quantity * 30 * 50  # 1 tray ≈ 30 eggs, 50g each
    elif measure == 'oil':
        #print(measure)
        return 'L' #quantity # 1 liter of oil ≈ 920 grams
    elif measure == 'grams':
        #print(measure)
        return 'g' #quantity  # Already in grams
    else:
        #print(measure)
        return '' #quantity 

def get_percentage(part, whole):
    return (part / whole) * 100 if whole else 0

def total_quantity_grams(materials):
    total_price = 0  # Initialize total price
    for mat in materials:
        price = BakeryPurchaseItems.objects.filter(raw_material=mat.raw_material).order_by('created').last()
        if price:  # Ensure price is not None
            total_price += price.price
    return total_price

def get_recipe(request):
    recipe_id = request.GET.get('recipe_id')
    output = float(request.GET.get('output', 1))  # Get the output value

    recipe = Recipe.objects.get(id=recipe_id)
    materials = RecipeRawMaterial.objects.filter(recipe=recipe)  # Assuming related field
    total_quantity_grams_value = total_quantity_grams(materials)  # Get the total quantity
    materials_data = []
    totals = {
        'total_quantity': 0, 'total_required_grams': 0, 'total_kg': 0,
        'total_price': 0, 'total_price_per_gram': 0, 'total_percentage_cost': 0, 'total_cost': 0,
    }

    for material in materials:
        quantity_grams = convert_to_grams(material.quantity_per_recipe, material.measure)
        required_grams = quantity_grams * Decimal(output)
        kg = convert_to_label(required_grams, material.raw_material.entry_measure,material.raw_material.raw_material_name)
        price= BakeryPurchaseItems.objects.filter(raw_material=material.raw_material).order_by('created').last()
        raw_price = price.price if price is not None else 0
        #raw_price = price.price or 0
        percent = get_percentage(raw_price, total_quantity_grams_value)
        
        total_price = (raw_price * kg)
        materials_data.append({
            'name': material.raw_material.raw_material_name,
            'quantity_grams': f"{round(quantity_grams, 2):,.2f}",
            'required_grams': f"{round(required_grams, 2):,.2f}",
            'kg': f"{round(kg, 2):,.2f}",
            'entryMeasure':name(material.raw_material.entry_measure),
            'price': f"{round(raw_price, 2):,.2f}",
            'price_per_gram': f"{round(raw_price / quantity_grams, 2):,.2f}" if quantity_grams else "0.00",
            'percentage_cost': f"{round(percent, 2):,.2f}",
            'total_cost': f"{round(total_price, 2):,.2f}",
            'total_qauntity':total_quantity_grams_value,
            
        })
        # print(materials_data)
       # Append to materials_data with rounded values (but numeric)


        # Accumulate totals (keep them as numbers)
        totals['total_quantity'] += quantity_grams
        totals['total_required_grams'] += required_grams
        # totals['total_kg'] += kg
        totals['total_price'] += raw_price
        totals['total_price_per_gram'] += raw_price / quantity_grams if quantity_grams else 0
        totals['total_percentage_cost'] += percent
        totals['total_cost'] += total_price

        # Format totals with comma separators for final display
        formatted_totals = {
            'total_quantity': f"{totals['total_quantity']:,.2f}",
            'total_required_grams': f"{totals['total_required_grams']:,.2f}",
            # 'total_kg': f"{totals['total_kg']:,.2f}",
            'total_price': f"{totals['total_price']:,.2f}",
            'total_price_per_gram': f"{totals['total_price_per_gram']:,.2f}",
            'total_percentage_cost': f"{totals['total_percentage_cost']:,.2f}",
            'total_cost': f"{totals['total_cost']:,.2f}",
        }


        # Example: Access formatted totals for display
        # print(formatted_totals)


    return JsonResponse({'materials': materials_data, 'totals': formatted_totals})

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Recipe
from .forms import RecipeForm  # Make sure to create a form for Recipe

# List View for Recipes
class RecipeListView(ListView):
    model = Recipe
    template_name = 'bakery/recipes/list.html'  # Update with your template path
    context_object_name = 'recipes'

# Create View for Adding Recipes
class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm  # Make sure you create this form
    template_name = 'bakery/recipes/add_edit.html'  # Update with your template path
    success_url = reverse_lazy('recipes')  # Redirect to the list view after successful addition

# Update View for Editing Recipes
class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm  # Make sure you create this form
    template_name = 'bakery/recipes/add_edit.html'  # Use the same form template for adding/editing
    success_url = reverse_lazy('recipes')  # Redirect to the list view after successful edit

    def get_object(self):
        recipe_id = self.kwargs.get('pk')
        return get_object_or_404(Recipe, pk=recipe_id)


def get_customer_name(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.GET.get('product_id')
        print(product_id)
        try:
            #product = BakeryCustomer.objects.get(id=product_id)
            product = get_object_or_404(BakeryInvoice, pk=product_id)
            print(product)
            customer_name = product.customer.customer_name
            customer_id = product.customer_id
            salesperson=product.sales_person
            session=product.sales_session
            try:
                total_paid = sum([item.amount_paid for item in product.bakeryinvoicepayment_set.all()])
                remaining = product.invoice_total - total_paid if product.invoice_total else 0
                if remaining < 0:
                    remaining = "Over paid"
            except AttributeError:
                remaining = product.invoice_total
            return JsonResponse({'customer_name': customer_name, 'id':customer_id,'remaining':remaining,'salesperson':salesperson,'session':session})
            # return JsonResponse({'price': customer_name, 'id':customer_id,'price2':product.invoice_total})
        except BakeryCustomer.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_product_price(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.GET.get('product_id')
        try:
            product = BakeryProduct.objects.get(id=product_id)
            return JsonResponse({'price': product.price})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_raw_price(request):
    if request.method == 'GET':
        rm_id = request.GET.get('rm_id')
        try:
            product = BakeryPurchaseItems.objects.filter(raw_material=rm_id).order_by('created').last()
            rawmat = RawMaterials.objects.get(pk=rm_id)
            print(rawmat.entry_measure)
            return JsonResponse({'price': product.price,'entryMeasure':rawmat.entry_measure,'unitPackaging':rawmat.weight_pack,'packaging':rawmat.packaging})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def add_more_row(request):
    formset = BakeryInvoiceDetailFormSet(prefix='form')
    empty_form = formset.empty_form
    rendered_row = render_to_string('bakery/invoice/new_row.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})


def add_more_row_purchase(request):
    formset = BakeryPurchaseItemsFormSet(prefix='form')
    empty_form = formset.empty_form
    rendered_row = render_to_string('bakery/purchases/new_row.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})

def add_more_row_inventory(request):
    formset = BakeryInventoryItemsFormSet(prefix='form')
    empty_form = formset.empty_form
    rendered_row = render_to_string('bakery/inventory/new_row.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})

def add_more_row_output(request):
    formset2 = BakeryProductionOutputFormset(prefix='form')
    empty_form = formset2.empty_form
    rendered_row = render_to_string('bakery/production/new_row_output.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})

from .forms import RecipeRawMaterialFormSet
def add_more_row_Recipe_rawmaterial(request):
    formset2 = RecipeRawMaterialFormSet(prefix='form')
    empty_form = formset2.empty_form
    rendered_row = render_to_string('bakery/reciperawmaterials/new_row_rawmaterial.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})


def production_output(request):
    # Fetch all production objects
    production = BakeryProduction.objects.all()
    
    # Extract all production IDs for the dropdown
    production_ids = production.values_list('production_id', flat=True)
    
    context = {
        'production': production,
        'production_ids': production_ids,  # Passing the production IDs to the template
    }
    return render(request, 'bakery/production/production_output.html', context)


from django.http import JsonResponse
from .models import BakeryProduction, BakeryProductionOutput, BakeryProduct, Recipe, RecipeRawMaterial, BakeryPurchaseItems
from decimal import Decimal
@login_required
def get_production_recipe(request):
    production_id = request.GET.get('production_id')
    
    try:
        # Fetch the BakeryProduction based on the provided production_id
        bakery_production = BakeryProduction.objects.get(production_id=production_id)
    except BakeryProduction.DoesNotExist:
        return JsonResponse({"error": "Invalid production ID"}, status=400)

    # Query BakeryProductionOutput for the specified production_id
    production_outputs = BakeryProductionOutput.objects.filter(production_id=bakery_production.pk)
    raw_usage=BakeryRawMaterialUsage.objects.filter(production_id=bakery_production.pk,status="Direct Usage")
    # Build data to return
    data = {
        "production": [],
        "weight":[],
        "raw_material_usage": [],
        "totals": {}
    }
    for raw in raw_usage:
        data["raw_material_usage"].append({
            "raw_material": raw.raw_material.raw_material_name,
            "entryMeasure": name(raw.raw_material.entry_measure),
            "entry": float(raw.qty) if raw.qty else 0,
            "quantityInGrams": convert_to_grams( raw.qty,raw.raw_material.entry_measure) if raw.raw_material_value else 0,
            "unit_cost_price": float(raw.unit_cost_price) if raw.unit_cost_price else 0,
            "total_cost_price": float(float(convert_to_grams( raw.qty,raw.raw_material.entry_measure) if raw.raw_material_value else 0)*(float(raw.unit_cost_price) if raw.unit_cost_price else 0)),
        })
    # Extract production details and related recipe details
    for output in production_outputs:
        # Fetch recipe details for each product
        product = BakeryProduct.objects.filter(id=output.product_id).first()  # Get the first matching product
        if product:
            recipe_details = get_recipe_production(product.recipe.id, output.qty)  # Fetch recipe details
           
            # Append each output and its recipe details to the materials list
            material_data = {
                "output_category": output.output_category,
                "mixture_number": output.mixture_number,
                "tag": output.tag,
                "product": product.product_name if product else "Unknown Product",
                "qty": float(output.qty) if output.qty else 0,
                "product_price": float(output.product_price) if output.product_price else 0,
                "value": float(output.value) if output.value else 0,
                "recipe_details": {"materials": recipe_details['materials'], "totals": recipe_details['totals']} if recipe_details else recipe_details['materials']['totals'],
               
            }
            data["production"].append(material_data)
            weight=BakeryProductUnitWeight.objects.get(product=product)
            # print(weight.product)
            data["weight"].append({
                
                    "product": weight.product.product_name,
                    "weight_per_boule": weight.weight_per_boul,
                    "output_per_boul": weight.output_per_boul,
                    "product_unit_weight": weight.product_unit_weight * output.qty,
                    "percentage": round((float(weight.product_unit_weight * output.qty) / sum(float(convert_to_grams(raw.qty, raw.raw_material.entry_measure) or 0) for raw in raw_usage)) * 100, 1),
                    "price": sum(float(raw["total_cost_price"]) for raw in data["raw_material_usage"]) * ((float(weight.product_unit_weight * output.qty) / sum(float(convert_to_grams(raw.qty, raw.raw_material.entry_measure) or 0) for raw in raw_usage)))
                
            })


    print(sum(float(material["product_unit_weight"]) for material in data["weight"] if material.get("product_unit_weight")))
    # Calculate totals
    data["totals"]["total_qty"] = sum(float(output.qty or 0) for output in production_outputs)
    data["totals"]["total_value"] = sum(float(output.value or 0) for output in production_outputs)
    data["totals"]["total_raw_material_grams"] = sum(float(convert_to_grams( raw.qty,raw.raw_material.entry_measure) or 0) for raw in raw_usage)
    data["totals"]["total_raw_material_price"] = sum(float(raw["total_cost_price"]) for raw in data["raw_material_usage"])
    data["totals"]["total_raw_material_remaining"] = data["totals"]["total_raw_material_grams"] - sum(float(material["product_unit_weight"]) for material in data["weight"] if material.get("product_unit_weight"))
    data["totals"]["total_raw_material_remaining_percentage"] = round((data["totals"]["total_raw_material_remaining"]/data["totals"]["total_raw_material_grams"])*100, 1)
    data["totals"]["total_raw_material_remaining_price"] = data["totals"]["total_raw_material_price"]*data["totals"]["total_raw_material_remaining_percentage"]/100
    return JsonResponse(data)
@login_required
def get_recipe_production(recipe_id, output_value):
    output = float(output_value)  # Get the output value

    recipe = Recipe.objects.get(id=recipe_id)
    materials = RecipeRawMaterial.objects.filter(recipe=recipe)  # Assuming related field
    materials_data = []
    totals = {
        'total_quantity': 0, 'total_required_grams': 0,
        'total_price': 0, 'total_cost': 0,
    }

    for material in materials:
        quantity_grams = convert_to_grams(material.quantity_per_recipe, material.measure)
        # print(material.quantity_per_recipe, material.measure)
        required_grams = quantity_grams * Decimal(output)
        kg = convert_to_label(required_grams, material.raw_material.entry_measure, material.raw_material.raw_material_name)
        price = BakeryPurchaseItems.objects.filter(raw_material=material.raw_material).order_by('created').last()
        raw_price = price.price if price else 0
        
        total_price = (raw_price * kg)
        materials_data.append({
            'ingredient': material.raw_material.raw_material_name,
            'quantity_grams': round(quantity_grams, 2),
            'required_grams': round(required_grams, 2),
            'kg': round(kg, 2),
            'entryMeasure': material.raw_material.entry_measure,
            'price': round(raw_price, 2),
            'total_cost': round(total_price, 2),
        })

        # Accumulate totals
        totals['total_quantity'] += quantity_grams
        totals['total_required_grams'] += required_grams
        totals['total_price'] += raw_price
        totals['total_cost'] += total_price

    # Return materials and totals
    return {
        'materials': materials_data,
        'totals': totals
    }


@login_required
def inventory_report(request):
    # form = BakeryRawMaterialUsageForm()
    # Filter inventory items based on raw_material (product_id)
    inventory_items = BakeryInventoryItems.objects.all()
    # Fetch unique raw materials from the filtered inventory items
    raw_materials = RawMaterials.objects.filter(id__in=inventory_items.values('raw_material_name_id'))
    context = {"raw_materials": raw_materials}
    return render(request, 'bakery/inventory/inventory_report.html', context)

def production_report(request):
    production_outputs = BakeryProductionOutput.objects.all()
    product_ids = production_outputs.values_list('product_id', flat=True).distinct()
    print(production_outputs)
    context = {"products": production_outputs}
    return render(request, 'bakery/production/production_report.html', context)
@login_required
def get_inventory_report(request):
    if request.method == 'GET':
        # Get filters from the request
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        selectedRawMaterialId=request.GET.get('selectedRawMaterialId')
        

        # Convert dates to datetime objects if provided
        start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

        print("start_date:", start_date)
        print("end_date:", end_date)
       

        # Filter inventory items based on raw_material (product_id)
        inventory_items = BakeryInventoryItems.objects.all()
        if start_date and end_date:
            inventory_items = inventory_items.filter(created__range=(start_date, end_date))
        if selectedRawMaterialId:
            inventory_items = inventory_items.filter(raw_material_name_id=selectedRawMaterialId)
        # Fetch unique raw materials from the filtered inventory items
        raw_materials = RawMaterials.objects.filter(id__in=inventory_items.values('raw_material_name_id'))

        # Prepare response data
        report_data = []
        report_data1=[]
        report_data2=[]

        for raw_material in raw_materials:
            print("Raw Material:", raw_material)

            # Opening inventory
            if start_date:
                opening_inventory = (
                    inventory_items.filter(raw_material_name=raw_material, created=start_date)
                    .aggregate(total_opening=Sum('quantity'))['total_opening'] or 0
                )
            else:
                opening_inventory = (
                    inventory_items.filter(raw_material_name=raw_material, status="Opening Stock")
                    .order_by('created')
                    .values_list('quantity', flat=True)
                    .first() or 0
                )

            print("opening_inventory:", opening_inventory)

            # Purchases
            if start_date and end_date:
                print("in if statement purchases")
                purchases = (
                    BakeryPurchaseItems.objects.filter(raw_material=raw_material, created__range=(start_date, end_date))
                    .aggregate(total_purchases=Sum('quantity'))['total_purchases'] or 0
                )
            else:
                purchases = (
                    BakeryPurchaseItems.objects.filter(raw_material=raw_material)
                    .aggregate(total_purchases=Sum('quantity'))['total_purchases'] or 0
                )

            print("purchases:", purchases)

            # Production raw material usage
            if start_date and end_date:
                print("in if statement RM usage")
                production_usage = (
                    BakeryRawMaterialUsage.objects.filter(raw_material=raw_material, created_at__range=(start_date, end_date))
                    .aggregate(total_usage=Sum('qty'))['total_usage'] or 0
                )

            else:
                production_usage = (
                    BakeryRawMaterialUsage.objects.filter(raw_material=raw_material)
                    .aggregate(total_usage=Sum('qty'))['total_usage'] or 0
                
                )

            print("production_usage:", production_usage)

            # Closing inventory
            if end_date:
                closure_inventory = (
                    inventory_items.filter(
                        raw_material_name=raw_material,
                        status="Closing Stock",
                        created=end_date
                    ).aggregate(total_closing=Sum('quantity'))['total_closing'] or 0)
            else:
                closure_inventory = (
                    inventory_items.filter(raw_material_name=raw_material, status="Closing Stock")
                    .order_by('-created')
                    .values_list('quantity', flat=True)
                    .first() or 0
                )
            print("closure_inventory:", closure_inventory)

            # Calculate expected closure and difference
            if opening_inventory and purchases and production_usage and closure_inventory:
                expected_closure = float(opening_inventory) + float(purchases) - float(production_usage)
                expected_difference = float(closure_inventory) - expected_closure
            else:
                expected_closure = float(opening_inventory) + float(purchases) - float(production_usage)
                expected_difference = float(closure_inventory) - expected_closure

            # print("expected_closure:", expected_closure)
            # print("expected_difference:", expected_difference)
            latest_purchase = BakeryPurchaseItems.objects.filter(raw_material=raw_material).order_by('-created').first()
            latest_price = float(latest_purchase.price if latest_purchase else 0)
            print(raw_material,latest_price)
            report_data1.append({
                'raw_material_id': raw_material.id,  # Include this field
                'raw_material': raw_material.raw_material_name,
                'opening_inventory': opening_inventory,
                'purchase': purchases,
                'production_usage': production_usage,
                'closing_inventory': closure_inventory,
                'expected_closing': expected_closure,
                'expected_difference': abs(expected_difference),
            })

            report_data2.append({
                'raw_material_id': raw_material.id,  # Include this field
                'raw_material': raw_material.raw_material_name,
                'opening_inventory': float(opening_inventory) * latest_price,
                'purchase': float(purchases) * latest_price,
                'production_usage': float(production_usage) * latest_price,
                'closing_inventory': float(closure_inventory) * latest_price,
                'expected_closing': float(expected_closure) * latest_price,
                'expected_difference': float(expected_difference) * latest_price,
            })
           
        return JsonResponse({'success': True, 'data1': report_data1,'data2': report_data2}, status=200)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)



from django.db.models import Sum
from datetime import datetime

def get_production_report(request):
    # Extract query parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    product_id = request.GET.get('product')
    # Convert dates to datetime objects if provided
    start_date = start_date if start_date else None
    end_date = end_date if end_date else None
    # Fetch all BakeryProductionOutput and their products
    production_outputs = BakeryProductionOutput.objects.all()
    if start_date and end_date:
        print("start_date:", start_date)
        print("end_date:", end_date)
        production_outputs = production_outputs.filter(created__range=(start_date, end_date))
    
    if product_id:
        print("product_id:", product_id)
        production_outputs = production_outputs.filter(product_id=product_id)
    product_ids = production_outputs.values_list('product_id', flat=True).distinct()
    products = BakeryProduct.objects.filter(id__in=product_ids)
    data = []

    for product in products:
        # Opening Stock
        opening_stock = production_outputs.filter(
            product=product,
            tag="Opening Stock"
        ).aggregate(total=Sum('qty'))['total'] or 0
        print("opening_stock:", opening_stock)

        # Production Output
        production_output = production_outputs.filter(
            product=product,
            tag="Production"
        ).aggregate(total=Sum('qty'))['total'] or 0
        print("production_output:", production_output)

        # Damages
        damages = BakeryConsumptionDamages.objects.filter(
            product=product,
            status="Damages",
            
        ).aggregate(total=Sum('qty'))['total'] or 0
        print("damages:", damages)

        # Consumption
        consumption = BakeryConsumptionDamages.objects.filter(
            product=product,
            status="Consumption",
        ).aggregate(total=Sum('qty'))['total'] or 0
        print("consumption:", consumption)

        # Sales
        sales = BakeryInvoiceDetail.objects.filter(
            product=product,
            invoice__in=BakeryInvoice.objects.filter(status="Sales"),
        ).aggregate(total=Sum('quantity'))['total'] or 0
        print("sales:", sales)

        # Returns Inwards
        returns = BakeryInvoiceDetail.objects.filter(
            product=product,
            invoice__in=BakeryInvoice.objects.filter(status="Return Inwards"),
        ).aggregate(total=Sum('quantity'))['total'] or 0
        print("returns:", returns)

        # Closing Stock
        closing_stock = production_outputs.filter(
            product=product,
            tag="Closing Stock"
        ).aggregate(total=Sum('qty'))['total'] or 0
        print("closing_stock:", closing_stock)

        # Expected Closing and Difference
        expected_closing = opening_stock + production_output + returns - damages - sales - consumption
        difference = abs(expected_closing - closing_stock)
        print("expected_closing:", expected_closing)
        print("difference:", difference)
        # Append product report data
        data.append({
            'product_name': product.product_name,
            'opening_stock': float(opening_stock),
            'production_output': float(production_output),
            'damages': float(damages),
            'consumption': float(consumption),
            'sales': float(sales),
            'returns': float(returns),
            'closing_stock': float(closing_stock),
            'expected_closing': float(expected_closing),
            'difference': float(difference),
        })

    return JsonResponse({'data': data}, safe=False)








# Create your views here.
def damages_view(request):
    invoices = BakeryConsumptionDamages.objects.all().order_by('-created_at')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        invoices = invoices.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('value')).values())[0]

    else:
        invoices = invoices
        total_invoice_amount = list(invoices.aggregate(Sum('value')).values())[0]

    template_name = 'bakery/damages/invoices.html'
    context = {
                'invoices':invoices,
                'total_invoice_amount':total_invoice_amount,
                'status':0,
                }
    return render(request, template_name, context)





#---------------------- Bakery Sales Invoice Detail ------------------#
# Detail view of invoices
def damages_detail(request, pk):

    invoice = BakeryConsumptionDamages.objects.get(id=pk)
    invoice_detail = BakeryConsumptionDamages.objects.filter(invoice=invoice)

    items = invoice.bakeryinvoicedetail_set.all()
    items_total = list(items.aggregate(Sum('total')).values())[0]

    # invoice_payments = invoice.bakeryinvoicepayment_set.all()
    # total_payments = list(invoice_payments.aggregate(Sum('amount_paid')).values())[0]
    # payment_installment_count = invoice_payments.count()

    # return_items = invoice.bakeryreturnsitems_set.all()
    # total_returns = list(return_items.aggregate(Sum('total')).values())[0]
    

    print(invoice)

    context = {
        'invoice': invoice,
        "invoice_detail": invoice_detail,
        #'items_total':items_total,
        # 'invoice_payments':invoice_payments,
        # 'total_payments':total_payments,
        # 'payment_installment_count':payment_installment_count,

        # "return_items":return_items,
        # 'total_returns':total_returns,

    }

    return render(request, "bakery/damages/invoice-template.html", context)


def create_damages(request):
    form = BakeryConsumptionDamagesForm()
    # formset = BakeryInvoiceDetailFormSet()
    if request.method == "POST":
        
        # Extract the main form data from the POST request
        production_id = request.POST.get("production_id")
        created = request.POST.get("created_at")
        sales_session = request.POST.get("session")
        sales_person = request.POST.get("employee")
        status = request.POST.get("status")
        sub_department=request.POST.get("sub_department")

        # Print the extracted values
        print(f"production_id: {production_id}")
        print(f"created: {created}")
        print(f"sales_session: {sales_session}")
        print(f"sales_person: {sales_person}")
        print(f"status: {status}")
        print(f"sub_department: {sub_department}")
        
        sub_department = get_object_or_404(SubDepartment, pk=sub_department)
        # Fetch the customer instance
        production = get_object_or_404(BakeryProduction, pk=production_id)

        # Print the customer instance to verify it's fetched correctly
        print(f"customer: {production}")

        # Create the invoice object
        if sales_person and production and created and sales_session:
            
            # Process each row of invoice details
            row_count = int(request.POST.get("row_count", 0))  # Number of rows
            print("row gotten: ", row_count)
            for i in range(1, row_count + 1):
                print("in for loop")
                product_id = int(request.POST.get(f"product_{i}"))
                quantity = float(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                print(f"product_id: {product_id}, quantity: {quantity}, price: {price}")
                product = get_object_or_404(BakeryProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price}")

                if  product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    print(f"Row {i} total: {row_total}")

                    # Create and save the BakeryInvoiceDetail
                    detail = BakeryConsumptionDamages.objects.create(
                        production_id=production,  # Assign the customer instance here
                        created_at=created,
                        session=sales_session,
                        employee=sales_person,
                        sub_department=sub_department,
                        status=status,
                        product=product,
                        qty=quantity,
                        product_price=price,
                    )
                    print(f"Saved detail for row {i}:", detail)

            # Save the total invoice amount
        

            print("Invoice total saved:", detail.value)

            # Optionally, return a JSON response indicating success
            return JsonResponse({"success": True, "invoice_id": detail.id})

        else:
            print("Error: Missing required invoice data")
            return JsonResponse({"success": False, "error": "Missing required invoice data"})

    # Handle GET requests or return an empty form for non-POST requests
    form = BakeryConsumptionDamagesForm()
    context = {
        "form": form,
        # 'formset': formset,
        }
    return render(request, "bakery/damages/create_invoice.html", context)


def edit_damage(request, pk):
    # Fetch the existing invoice using the provided primary key (pk)
    invoice = get_object_or_404(BakeryConsumptionDamages, id=pk)
    
    if request.method == "POST":
        # Extract main form data from the POST request
        production_id = request.POST.get("production_id")
        created = request.POST.get("created_at")
        sales_session = request.POST.get("session")
        sales_person = request.POST.get("employee")
        status = request.POST.get("status")
        sub_department = request.POST.get("sub_department")

        # Fetch the necessary objects based on the IDs
        sub_department = get_object_or_404(SubDepartment, pk=sub_department)
        production = get_object_or_404(BakeryProduction, pk=production_id)

        # Update the invoice object with the new data
        if production and created and sales_session and sales_person:
            # Process each row of invoice details
            row_count = int(request.POST.get("row_count", 0))  # Number of rows
            for i in range(1, row_count + 1):
                product_id = int(request.POST.get(f"product_{i}"))
                quantity = float(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                

                # Fetch the product instance
                product = get_object_or_404(BakeryProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price}")
                invoice_details = BakeryConsumptionDamages.objects.filter(id=pk)
                if product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    # total += row_total  # Add to the total invoice amount

                    # Update or create the corresponding BakeryConsumptionDamages entry
                    if i <= len(invoice_details):
                        detail = invoice_details[i - 1]
                        detail.production_id = production  # Update the production reference
                        detail.created_at = created  # Update the created date
                        detail.session = sales_session  # Update session
                        detail.employee = sales_person  # Update employee
                        detail.status = status  # Update status
                        detail.sub_department = sub_department 
                        detail.product = product
                        detail.qty = quantity
                        detail.product_price = price
                        detail.value = row_total
                        detail.save()
                        print(f"Updated detail for row {i}: {detail.qty}")
                    else:
                        # If there are fewer details than rows, create new ones
                        detail = BakeryConsumptionDamages.objects.create(
                            production_id=production,  # Assign the production instance
                            created_at=created,
                            session=sales_session,
                            employee=sales_person,
                            sub_department=sub_department,
                            status=status,
                            product=product,
                            qty=quantity,
                            product_price=price,
                            
                        )
                        print(f"Created new detail for row {i}: {detail}")

            # Save the total invoice amount (if needed)
            # invoice_details.save()
            # print(f"Invoice total saved: {invoice_details.value}")

            # Optionally, return a JSON response indicating success
            return JsonResponse({"success": True, "invoice_id": invoice.pk})

        else:
            print("Error: Missing required invoice data")
            return JsonResponse({"success": False, "error": "Missing required invoice data"})

    # Handle GET requests or return the form pre-filled with the existing invoice details
    form = BakeryConsumptionDamagesForm(instance=invoice)
    context = {
        "form": form,
        # 'formset': formset,
        "invoice": invoice,  # Pass the invoice to the template if needed
    }
    return render(request, "bakery/damages/edit_invoice.html", context)


def add_more_row_damage(request):
    formset = BakeryConsumptionDamagesForm()
    empty_form = formset
    rendered_row = render_to_string('bakery/damages/new_row.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})
