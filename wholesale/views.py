from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
#from .forms import *
from django.db.models import Sum
from django.db.models import Q

from .models import *
from customer.models import *
from product.models import *
# Create your views here.

from .forms import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Invoice view


@login_required
def wholesale_view(request):
    # Your homepage logic (e.g., display featured content)
    return render(request, 'wholesale/wholesale.html')




class WholesaleProductListView(ListView):
    model = WholesaleProduct
    template_name = 'wholesale/product/list.html'
    context_object_name = 'products'

class WholesaleProductCreateView(CreateView):
    model = WholesaleProduct
    template_name = 'wholesale/product/add.html'
    fields = '__all__'  # or specify the fields you want to include
    success_url = reverse_lazy('wholesale:product-list')  # Redirect after successful creation

class WholesaleProductUpdateView(UpdateView):
    model = WholesaleProduct
    template_name = 'wholesale/product/add.html'
    fields = '__all__'  # or specify the fields you want to include
    success_url = reverse_lazy('wholesale:product-list')  # Redirect after successful update




# class ProductRecipeListView(ListView):
#     model = ProductRecipe
#     template_name = 'wholesale/recipe/list.html'
#     context_object_name = 'product_recipes'

# class ProductRecipeCreateView(CreateView):
#     model = ProductRecipe
#     template_name = 'wholesale/recipe/add_edit.html'
#     fields = ['product', 'recipe', 'quantity_per_product']

#     def form_valid(self, form):
#         form.save()
#         return redirect('wholesale:productrecipe-list')


# class ProductRecipeUpdateView(UpdateView):
#     model = ProductRecipe
#     template_name = 'wholesale/recipe/add_edit.html'
#     fields = ['product', 'recipe', 'quantity_per_product']

#     def form_valid(self, form):
#         form.save()
#         return redirect('wholesale:productrecipe-list')



# #Raw materials
# from django.shortcuts import redirect
# from django.urls import reverse_lazy
# from django.views.generic import ListView, CreateView, UpdateView
# from .models import RawMaterials

# class RawMaterialsListView(ListView):
#     model = RawMaterials
#     template_name = 'wholesale/raw_materials/list.html'
#     context_object_name = 'raw_materials'

# class RawMaterialsCreateView(CreateView):
#     model = RawMaterials
#     template_name = 'wholesale/raw_materials/add_edit.html'
#     fields = '__all__'

#     def form_valid(self, form):
#         form.save()
#         return redirect('wholesale:raw-materials-list')

# class RawMaterialsUpdateView(UpdateView):
#     model = RawMaterials
#     template_name = 'wholesale/raw_materials/add_edit.html'
#     fields = '__all__'

#     def form_valid(self, form):
#         form.save()
#         return redirect('wholesale:raw-materials-list')


# #ecipe raw materials
# from django.views.generic import ListView, CreateView, UpdateView
# from .models import RecipeRawMaterial

# class RecipeRawMaterialListView(ListView):
#     model = RecipeRawMaterial
#     template_name = 'wholesale/reciperawmaterials/list.html'
#     context_object_name = 'wholesale:recipe_raw_materials'

# class RecipeRawMaterialCreateView(CreateView):
#     model = RecipeRawMaterial
#     template_name = 'wholesale/reciperawmaterials/add_edit.html'
#     fields = ['recipe', 'raw_material', 'quantity_per_recipe', 'measure']

#     def form_valid(self, form):
#         form.save()
#         return redirect('wholesale:reciperawmaterial-list')


# class RecipeRawMaterialUpdateView(UpdateView):
#     model = RecipeRawMaterial
#     template_name = 'wholesale/reciperawmaterials/add_edit.html'
#     fields = ['recipe', 'raw_material', 'quantity_per_recipe', 'measure']

#     def form_valid(self, form):
#         form.save()
#         return redirect('wholesale:reciperawmaterial-list')

#############   #############   #############   #############   #############
#------------------------- Customer Views ------------------------------#
#############   #############   #############   #############   #############
class WholesaleCustomerListView(ListView):
    model = WholesaleCustomer
    template_name = 'wholesale/wholesale_customer/customers.html'  # Specify your template name
    context_object_name = 'customers'  # The name to use in the template
    paginate_by = 1000  # Number of customers per page

    def get_queryset(self):
        return WholesaleCustomer.objects.all().order_by('customer_name')  # Order by customer name

    
class WholesaleCustomerDetailView(DetailView):
    model = WholesaleCustomer
    template_name = 'wholesale/wholesale_customer/customer_account.html'  # Specify your template name
    context_object_name = 'customer'  # The name to use in the template
    slug_field = 'slug'  # Use slug field for URL lookup
    slug_url_kwarg = 'slug'  # The name of the slug URL parameter

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(WholesaleCustomer, slug=slug)
    
class WholesaleCustomerCreateView(View):
    def get(self, request):
        form = WholesaleCustomerForm()
        return render(request, 'wholesale/wholesale_customer/add_customer_form.html', {'form': form})

    def post(self, request):
        form = WholesaleCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wholesale:customer')  # Redirect to customer list after successful creation
        return render(request, 'wholesale/wholesale_customer/add_customer_form.html', {'form': form})  
    
class WholesaleCustomerEditView(UpdateView):
    model = WholesaleCustomer
    form_class = WholesaleCustomerForm
    template_name = 'wholesale/wholesale_customer/edit_customer_form.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(WholesaleCustomer, slug=slug)

    def form_valid(self, form):
        form.save()
        return redirect('wholesale:customer')  # Redirect to the customer list after saving    
    
#############   #############   #############   #############   #############
#------------------------- Product Views ------------------------------#
#############   #############   #############   #############   ############# 
class WholesaleProductCategoryListView(ListView):
    model = WholesaleProductSubCategory
    template_name = 'wholesale/wholesale_product/categories.html'  # Specify your template name
    context_object_name = 'categories'  # The name to use in the template
    paginate_by = 10  # Number of categories per page

    def get_queryset(self):
        return WholesaleProductSubCategory.objects.all().order_by('sub_category_name')  # Order by category name


class WholesaleProductCategoryDetailView(DetailView):
    model = WholesaleProductSubCategory
    template_name = 'wholesale/wholesale_product/category_detail.html'  # Specify your template name
    context_object_name = 'category'  # The name to use in the template
    slug_field = 'slug'  # Use slug field for URL lookup
    slug_url_kwarg = 'slug'  # The name of the slug URL parameter


class WholesaleProductCategoryCreateView(CreateView):
    model = WholesaleProductSubCategory
    form_class = WholesaleProductCategoryForm  # Ensure you have a form for this model
    template_name = 'wholesale/wholesale_product/add_category_form.html'  # Specify your template name

    def form_valid(self, form):
        form.save()
        return redirect('wholesale:category-list')  # Redirect to category list after successful creation
    


class WholesaleProductCategoryEditView(UpdateView):
    model = WholesaleProductSubCategory
    form_class = WholesaleProductCategoryForm
    template_name = 'wholesale/wholesale_product/edit_category_form.html'  # Specify your template name

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(WholesaleProductSubCategory, pk=pk)

    def form_valid(self, form):
        form.save()
        return redirect('wholesale:category-list')  # Redirect to the category list after saving

#Customer opening

class WholesaleCustomerOpeningBalanceListView(ListView):
    model = WholesaleOpeningBalance
    template_name = 'wholesale/customer_opening_balance/list.html'
    context_object_name = 'customer_opening_balances'

class WholesaleCustomerOpeningBalanceCreateView(CreateView):
    model = WholesaleOpeningBalance
    template_name = 'wholesale/customer_opening_balance/add_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('wholesale:customer-opening-balance-list')

class WholesaleCustomerOpeningBalanceUpdateView(UpdateView):
    model = WholesaleOpeningBalance
    template_name = 'wholesale/customer_opening_balance/add_edit.html'
    fields ='__all__'
    success_url = reverse_lazy('wholesale:customer-opening-balance-list')


# class WholesaleReturnsItemsListView(ListView):
#     model = WholesaleReturnsItems
#     template_name = 'wholesale/invoice/returns-list.html'
#     context_object_name = 'return_items'

#     def get_queryset(self):
#         # Ensure that related `customer` objects are properly fetched
#         return super().get_queryset().select_related('customer')

# # class WholesaleReturnsItemsCreateView(CreateView):
# #     model = WholesaleReturnsItems
# #     template_name = 'wholesale/customer_return_items_form.html'
# #     fields = ['date', 'customer', 'invoice', 'product', 'quantity', 'price', 'total']
# #     success_url = reverse_lazy('wholesale:customer-return-items-list')

# class WholesaleReturnsItemsUpdateView(UpdateView):
#     model = WholesaleReturnsItems
#     template_name = 'wholesale/invoice/edit-returns.html'
#     fields = ['date', 'customer', 'invoice', 'product', 'quantity', 'price', 'total']
#     success_url = reverse_lazy('wholesale:customer-return-items-list')

# #--------------------------------------------------------#

# Create your views here.
def invoice_view(request):
    invoices = WholesaleInvoice.objects.all()
    invoices = invoices.annotate(discount=Sum('wholesaleinvoicedetail__discount_value'))
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        invoices = invoices.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('invoice_total')).values())[0]

    else:
        invoices = invoices
        total_invoice_amount = list(invoices.aggregate(Sum('invoice_total')).values())[0]

    template_name = 'wholesale/invoice/invoices.html'
    context = {
                'invoices':invoices,
                'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)

# Detail view of invoices
def invoice_detail(request, pk):

    invoice = WholesaleInvoice.objects.get(id=pk)
    invoice_detail = WholesaleInvoiceDetail.objects.filter(invoice=invoice)

    items = invoice.wholesaleinvoicedetail_set.all()
    items_total = list(items.aggregate(Sum('total_selling_price')).values())[0]

    invoice_payments = invoice.wholesaleinvoicepayment_set.all()
    total_payments = list(invoice_payments.aggregate(Sum('amount_paid')).values())[0]
    payment_installment_count = invoice_payments.count()

    # return_items = invoice.wholesalereturnsitems_set.all()
    # total_returns = list(return_items.aggregate(Sum('total')).values())[0]

    print(invoice)

    context = {
        'invoice': invoice,
        "invoice_detail": invoice_detail,
        "items_total":items_total,
        'invoice_payments':invoice_payments,
        'total_payments':total_payments,
        'payment_installment_count':payment_installment_count,

        # "return_items":return_items,
        # 'total_returns':total_returns,

    }

    return render(request, "wholesale/invoice/invoice-template.html", context)

from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta, date
def create_invoice(request):
    form = WholesaleInvoiceForm()
    formset = WholesaleInvoiceDetailFormSet()
    if request.method == "POST":
        
        supplier_id=int(request.POST.get("customer"))
        created=request.POST.get("created")
        
        status = request.POST.get("status")
        print(f"supplier_id (after conversion): {supplier_id}")
        # print(f"department (after conversion): {department}")
        supplier = get_object_or_404(WholesaleCustomer, pk=supplier_id)
        print(f"supplier_id: {supplier}")
        print(f"created: {created}")
        # print(f"department: {department}")
        print(f"status: {status}")
        print(f"supplier: {supplier} ")

        if supplier and status and created:
            invoice = WholesaleInvoice.objects.create(
                customer=supplier,  # Assign the customer instance here
                created=created,
                
                status=status
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
                product_id = request.POST.get(f"product_{i}")
                quantity = int(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                discount_price = float(request.POST.get(f"discount_amount_{i}", 0))
                delivery_man = request.POST.get(f"delivery_man_{i}")

                product = get_object_or_404(WholesaleProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},Discount amount: {discount_price}")

                if  product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    # Create and save the WholesaleInvoiceDetail
                    detail = WholesaleInvoiceDetail.objects.create(
                        invoice=invoice,
                        product=product,
                        quantity=quantity,
                        total_selling_price=price,
                        discount_price=discount_price,
                        delivery_man=delivery_man,
                        
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
    form = WholesaleInvoiceForm()
    context = {
        "form": form,
        'formset': formset,
        }
    return render(request, "wholesale/invoice/create_invoice.html", context)


#--------------------------------------------------------------------#
@login_required
def edit_invoice(request, pk):
    print("edit_invoice() called with pk:", pk)

    print("edit_invoice() - Fetching invoice and associated details")
    invoice = get_object_or_404(WholesaleInvoice, pk=pk)
    print(f"invoice: {invoice}")
    invoice_items = WholesaleInvoiceDetail.objects.filter(invoice=invoice)
    print(f"invoice_items: {invoice_items}")

    # Create a model formset for WholesaleInvoiceDetail
    WholesaleInvoiceDetailFormSet = modelformset_factory(
        WholesaleInvoiceDetail,
        form=WholesaleInvoiceDetailForm,
        extra=0,
        can_delete=True
    )
    print(f"WholesaleInvoiceDetailFormSet: {WholesaleInvoiceDetailFormSet}")
    form = WholesaleInvoiceForm(instance=invoice)
    # print(f"form: {form}")
    formset = WholesaleInvoiceDetailFormSet(queryset=invoice_items)
    # print(f"formset: {formset}")
    if request.method == "POST":
        # Extract the main form data from the POST request
        supplier_id = int(request.POST.get("customer"))
        created = request.POST.get("created")
        status = request.POST.get("status")

        # Fetch the supplier instance
        supplier = get_object_or_404(WholesaleCustomer, pk=supplier_id)
        print(f"supplier: {supplier}")

        # Update the invoice object
        if supplier and status and created:
            invoice.customer = supplier
            invoice.created = created
            invoice.status = status
            invoice.save()
            print("Invoice updated:", invoice)

            # Initialize total
            total = 0
            print("init total : ", total)

            # Process each row of invoice details
            row_count = int(request.POST.get("row_count", 0))  # Number of rows
            print("row gotten: ", row_count)

            for i in range(1, row_count + 1):
                print("Processing row:", i)
                # Retrieve form data for the current row
                product_id = request.POST.get(f"product_{i}")
                quantity = int(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                discount_price = float(request.POST.get(f"discount_price_{i}", 0))
                detail_id = int(request.POST.get(f"id_{i}", 0))

                if not product_id:
                    print(f"Skipping row {i} due to missing product_id")
                    continue

                product = get_object_or_404(WholesaleProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price}, Discount Price: {discount_price}")

                if quantity and price:
                    discount_value = quantity * discount_price
                    # Calculate the sum for each row
                    row_total = (price * quantity) - discount_value
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    # Update or create the WholesaleInvoiceDetail
                    if i <= len(invoice_items):
                        detail = invoice_items[i-1]  # Update existing detail
                        detail.product = product
                        detail.quantity = quantity
                        detail.unit_selling_price = price
                        detail.discount_price = discount_price
                        
                        detail.save()
                        print(f"Updated detail for row {i}: {detail}")
                    else:
                        # If there are fewer details than rows, create new ones
                        detail = WholesaleInvoiceDetail.objects.create(
                            invoice=invoice,
                            product=product,
                            quantity=quantity,
                            unit_selling_price=price,
                            discount_price=discount_price,
                            discount_value=discount_value,
                            net_amount=row_total,
                        )
                        print(f"Created new detail for row {i}: {detail}")
                    print(f"Saved detail for row {i}: {detail}")

            # Save the total invoice amount
            invoice.invoice_total = total
            invoice.save()
            print("Invoice total saved:", invoice.invoice_total)

            # Optionally, return a JSON response indicating success
            return JsonResponse({"success": True, "invoice_id": invoice.id})

        else:
            print("Error: Missing required invoice data")
            return JsonResponse({"success": False, "error": "Missing required invoice data"})

    context = {
        'form': form,
        'formset': formset,
        'invoice': invoice,
    }
    return render(request, 'wholesale/invoice/edit_invoice.html', context)



# Invoice view
def InvoicePayment_view(request):
        invoice = WholesaleInvoice.objects.all()
        customer = Customer.objects.all()
        invoice_payment = WholesaleInvoicePayment.objects.all().order_by('-date')
        #invoice_grand_total = list(invoices.aggregate(Sum('grand_total')).values())[0]

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date:
            invoice_payment = invoice_payment.filter(created__range=[start_date, end_date])
        else:
            invoice_payment = WholesaleInvoicePayment.objects.all().order_by('-date')
            #total_orders = list(invoices.aggregate(Sum('amount')).values())[0]
        for payment in invoice_payment:
            print("Invoice payment:", payment.invoice)
        template_name = 'wholesale/invoice/invoice_payments.html'
        context = {
                    'invoice_payment':invoice_payment,
                    "invoice":invoice,
                    "customer":customer ,

                    }
        return render(request, template_name, context)

class add_payment_view(SuccessMessageMixin, CreateView):
        model = WholesaleInvoicePayment
        template_name = 'wholesale/invoice/add_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("wholesale:invoice-payments")
        success_message = 'Payment Transaction successful'

# Invoice view
class edit_payment_view(SuccessMessageMixin, UpdateView):
        model = WholesaleInvoicePayment
        template_name = 'wholesale/invoice/edit_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("wholesale:invoice-payments")
        success_message = 'Payment Transaction successfully Updated'

        # def get_object(self, queryset=None):
        #         # Get the payment by id (pk) from the URL
        #         payment_id = self.kwargs.get('pk')
        #         # Store the payment in a variable
        #         payment = WholesaleInvoicePayment.objects.get(id=payment_id)
        #         print(payment)
        #         return payment

        # def get_context_data(self, **kwargs):
        #     # Call the base implementation to get the context
        #     context = super().get_context_data(**kwargs)
        #     # Add the payment object to the context
        #     context['payment'] = self.get_object()
        #     return context
# class add_returns_view(SuccessMessageMixin, CreateView):
#         model = WholesaleReturnsItems
#         template_name = 'wholesale/invoice/add_returns.html'
#         fields = '__all__'
#         #exclude = ('slug',)
#         success_url = reverse_lazy('wholesale:invoice-payments')
#         success_message = 'Payment Transaction successful'



########################PURCHASES##############
# Create your views here.
@login_required
def purchases_view(request):
    purchases = WholesalePurchase.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    print(purchases)
    if start_date:
        purchases = purchases.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(purchases.filter(created__range=[start_date, end_date]).aggregate(Sum('purchase_total')).values())[0]

    else:
        purchases = purchases
        total_invoice_amount = list(purchases.aggregate(Sum('purchase_total')).values())[0]

    template_name = 'wholesale/purchases/purchase_invoices.html'
    context = {
                'purchases':purchases,
                'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)
 
    #--------------------------------------------------------#
    # Detail view of invoices
@login_required
def purchase_detail(request, pk):

    invoice = WholesalePurchase.objects.get(id=pk)
    purchases_detail = WholesalePurchaseItems.objects.filter(purchase_id=invoice)

    #items = invoice.invoicedetail_set.all()
    #items_total = list(items.aggregate(Sum('total')).values())[0]

    # purchase_invoice_payments = invoice.purchaseinvoicespayment_set.all()
    # total_payments = list(purchase_invoice_payments.aggregate(Sum('amount_paid')).values())[0]
    #payment_installment_count = invoice_payments.count()
    # print(total_payments)
    #return_items = invoice.returnsitems_set.all()
    #total_returns = list(return_items.aggregate(Sum('total')).values())[0]



    context = {
        'purchase': invoice,
        "purchases_detail": purchases_detail,
        #'items_total':items_total,
        # 'purchase_invoice_payments':purchase_invoice_payments,
        # 'total_payments':total_payments,
        #'payment_installment_count':payment_installment_count,

        #"return_items":return_items,
        #'total_returns':total_returns,

    }

    return render(request, "wholesale/purchases/purchases-invoice-template.html", context)
#---------------------------------------------------------------------------------------#
# WholesaleInvoice view
@login_required
def create_purchase(request):

    form = WholesalePurchaseForm()
    formset = WholesalePurchaseItemsFormSet(queryset=WholesalePurchase.objects.none())
    if request.method == "POST":
        
        supplier_id=int(request.POST.get("supplier_name"))
        created=request.POST.get("created")
        employee = request.POST.get("employee")
        status = request.POST.get("status")
        print(f"supplier_id (after conversion): {supplier_id}")
        # print(f"department (after conversion): {department}")
        # supplier = WholesaleSupplier.objects.filter(id=supplier_id)
        supplier = WholesaleSupplier.objects.get(id=supplier_id)

        print(f"supplier_id: {supplier}")
        print(f"created: {created}")
        # print(f"department: {department}")
        print(f"sales_session: {employee}")
        print(f"supplier: {supplier} ")
 
        if supplier and employee and created:
            invoice = WholesalePurchase.objects.create(
                supplier_name=supplier,  # Assign the customer instance here
                created=created,
               
                status=status,
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
                product_id = request.POST.get(f"product_{i}")
                quantity = int(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                discount_price = float(request.POST.get(f"discount_amount_{i}", 0))

                product = get_object_or_404(WholesaleProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},Discount amount: {discount_price}")

                if  product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    # Create and save the WholesaleInvoiceDetail
                    detail = WholesalePurchaseItems.objects.create(
                        purchase_id=invoice,
                        product=product,
                        quantity=quantity,
                        price=price,
                        discount_amount=discount_price,
                        
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

        #return redirect("wholesale:purchases")

    context = {

        #"total_invoice": total_invoice,
        "form": form,
        "formset": formset,
    }

    return render(request, "wholesale/purchases/create_purchase.html", context)
#--------------------------------------------------------------------#
@login_required
def edit_purchase(request, pk):
    # Fetch the existing invoice and its items
    invoice = get_object_or_404(WholesalePurchase, pk=pk)
    invoice_items = WholesalePurchaseItems.objects.filter(purchase_id=invoice)
    WholesalePurchaseItemsFormSet = modelformset_factory(WholesalePurchaseItems, form=WholesalePurchaseItemsForm, extra=0, can_delete=True)

    # Initialize the forms with existing invoice data
    form = WholesalePurchaseForm(instance=invoice)
    formset = WholesalePurchaseItemsFormSet(queryset=invoice_items)

    if request.method == "POST":
        supplier_id = int(request.POST.get("supplier_name"))
        created = request.POST.get("created")
        employee = request.POST.get("employee")
        status = request.POST.get("status")

        # Fetch the supplier instance
        supplier = get_object_or_404(WholesaleSupplier, pk=supplier_id)

        if supplier and employee and created:
            invoice.supplier_name = supplier
            invoice.created = created
            invoice.status = status
            invoice.employee = employee
            invoice.save()
            print("Invoice updated:", invoice)

            total = 0
            row_count = int(request.POST.get("row_count", 0))

            for i in range(1, row_count + 1):
                detail = invoice_items[i-1] if i-1 < len(invoice_items) else (invoice_items.first() if invoice_items.exists() else None)

                product_id = request.POST.get(f"product_{i}")
                quantity = int(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                discount_price = float(request.POST.get(f"discount_amount_{i}", 0))

                product = get_object_or_404(WholesaleProduct, pk=product_id)

                if product and quantity and price:
                    row_total = price * quantity
                    total += row_total

                    if i <= len(invoice_items):
                        detail = invoice_items[i-1]
                        detail.product = product
                        detail.quantity = quantity
                        detail.price = price
                        detail.discount_amount = discount_price
                        detail.save()
                        print(f"Updated detail for row {i}: {detail}")
                    else:
                        detail = WholesalePurchaseItems.objects.create(
                            purchase_id=invoice,
                            product=product,
                            quantity=quantity,
                            price=price,
                            discount_amount=discount_price
                        )
                        print(f"Created new detail for row {i}: {detail}")

            invoice.purchase_total = total
            invoice.save()
            print("Invoice total updated:", invoice.purchase_total)

            return JsonResponse({"success": True, "invoice_id": invoice.id})

        else:
            print("Error: Missing required invoice data")
            return JsonResponse({"success": False, "error": "Missing required invoice data"})

    context = {
        "form": form,
        "formset": formset,
        "invoice": invoice,
    }

    return render(request, "wholesale/purchases/create_purchase.html", context)

# WholesaleInvoice view
@login_required
def purchase_invoice_payments_view(request):
        invoice = WholesaleInvoice.objects.all()
        supplier = WholesaleSupplier.objects.all()
        purchase_invoice_payment = WholesaleInvoicePayment.objects.all().order_by('-date')
        #invoice_grand_total = list(invoices.aggregate(Sum('grand_total')).values())[0]

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date:
            purchase_invoice_payment = purchase_invoice_payment.filter(created__range=[start_date, end_date])
            #total_orders = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('amount')).values())[0]

        else:
            purchase_invoice_payment = purchase_invoice_payment
            #total_orders = list(invoices.aggregate(Sum('amount')).values())[0]

        template_name = 'wholesale/purchases/purchase_invoice_payments.html'
        context = {
                    'purchase_invoice_payment':purchase_invoice_payment,
                    "invoice":invoice,
                    "supplier":supplier ,

                    }
        return render(request, template_name, context)
    
class add_purchase_payment_view(SuccessMessageMixin, CreateView):
        model = WholesaleInvoicePayment
        template_name = 'wholesale/purchases/add_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("wholesale:purchases")
        success_message = 'Payment Transaction successful'

# WholesaleInvoice view
class edit_purchase_payment_view(SuccessMessageMixin, UpdateView):
        model = WholesaleInvoicePayment
        template_name = 'wholesale/purchases/edit_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("wholesale:purchases")
        success_message = 'Payment Transaction successfully Updated'







###################################SUPPLIER############################

# Create your views here.
@login_required
def suppliers_view(request):
    suppliers = WholesaleSupplier.objects.all()

    template_name = 'wholesale/supplier/suppliers.html'
    context = {'suppliers':suppliers}
    return render(request, template_name, context)
#-------------------------------------------------------------------#
@login_required
def supplier_details(request, id):#
    supplier = get_object_or_404(WholesaleSupplier, id=id)

    supplier_invoice = supplier.wholesalepurchase_set.filter(status='Purchases')
    supplier_invoice_total = list(supplier_invoice.aggregate(Sum('purchase_total')).values())[0]

    purchase_returns = supplier.wholesalepurchase_set.filter(status='Return Outwards')
    total_purchase_returns= list(purchase_returns.aggregate(Sum('purchase_total')).values())[0]

    if supplier_invoice_total is not None and total_purchase_returns is not None:
        account_balance = supplier_invoice_total - total_purchase_returns
    else:
        account_balance = 0.00

    template_name = 'wholesale/supplier/supplier_account.html'
    context = {'supplier':supplier,
                'supplier_invoice':supplier_invoice,
                'supplier_invoice_total':supplier_invoice_total,

                'purchase_returns':purchase_returns,
                'total_purchase_payment':total_purchase_returns,
                'account_balance':account_balance,
                }
    return render(request, template_name, context)
#-------------------------------------------------------------------------#
class add_supplier(SuccessMessageMixin, CreateView):
    model = WholesaleSupplier
    template_name = 'wholesale/supplier/forms/add_supplier.html'
    fields = '__all__'
    exclude = ('slug',)
    success_url = reverse_lazy('wholesale:supplier')
    success_message = 'supplier Account Successfully Created !!!'

#-------------------------------------------------------------------------#
class edit_supplier(SuccessMessageMixin, UpdateView):
    model = WholesaleSupplier
    template_name = 'wholesale/supplier/forms/edit_supplier.html'
    fields = '__all__'
    exclude = ('slug',)
    success_url = reverse_lazy('wholesale:supplier')
    success_message = 'supplier Account Successfully Edited !!!'
#-------------------------------------------------------------------------#


# #--------------------------- Production --------------------------------#
# #----- Production List -------#
# class WholesaleProductionListView(ListView):
#     model = WholesaleProduction
#     template_name = 'wholesale/production/production_list.html'
#     context_object_name = 'production'

# #----- Create Production -------#
# def create_production(request):
#     # Initialize the form for the main WholesaleProduction details
#     form = WholesaleProductionForm()
#     # Initialize the formset for handling multiple raw material usages
#     formset = WholesaleRawMaterialUsageFormSet(queryset=WholesaleProduction.objects.none())
#     formset2 = WholesaleProductionOutputFormset(queryset=WholesaleProductionOutput.objects.none())

#     # Check if the request is a POST request (form submission)
#     if request.method == "POST":
#         # Extract individual fields from the POST request data
#         created_at = request.POST.get("created_at")
#         mixture_number = request.POST.get("mixture_number")
#         department = "Wholesale"
#         sub_department_id = request.POST.get("sub_department")
#         session = request.POST.get("session")
#         supervisor = request.POST.get("supervisor")
#         stock_supervisor = request.POST.get("stock_supervisor")

#         # Print the values
#         print("Created At:", created_at)
#         print("Mixture Number:", mixture_number)
#         print("Department:", department)
#         print("Sub Department ID:", sub_department_id)
#         print("Session:", session)
#         print("Supervisor:", supervisor)
#         print("Stock Supervisor:", stock_supervisor)

#         # Fetch the SubDepartment instance based on the provided ID
#         sub_department = get_object_or_404(SubDepartment, pk=sub_department_id)
#         print("Sub Department:", sub_department)

#         # Check if all the required fields are present before creating a WholesaleProduction object
#         if created_at and mixture_number and department and sub_department and session and supervisor and stock_supervisor:
#             # Create a new WholesaleProduction object with the provided data
#             production = WholesaleProduction.objects.create(
#                 created_at=created_at,
#                 mixture_number=mixture_number,
#                 department=department,
#                 sub_department=sub_department,
#                 session=session,
#                 supervisor=supervisor,
#                 stock_supervisor=stock_supervisor
#             )
#             print("Production created:", production)  # Debugging statement to confirm creation
            
#             # Initialize the total raw material usage cost to 0
#             total = 0
#             print("total gotten")  # Debugging statement to confirm total initialization
            
#             # Get the total number of rows of raw material data from the POST request
#             row_count = int(request.POST.get("row_count", 0))
#             print("row gotten: ", row_count)  # Debugging statement to confirm row count retrieval
            
#             # Loop through each row of raw material data submitted
#             for i in range(1, row_count + 1):
#                 print("in for loop")  # Debugging statement to confirm entering the loop
                
#                 # Extract the product ID, quantity, and price from the POST data for each row
#                 product_id = request.POST.get(f"product_{i}")
#                 quantity = int(request.POST.get(f"quantity_{i}", 0))
#                 price = float(request.POST.get(f"price_{i}", 0))
#                 print(f"Product ID {i}:", product_id)
#                 print(f"Quantity {i}:", quantity)
#                 print(f"Price from form {i}:", price)
#                 # Fetch the RawMaterials instance using the extracted product ID
#                 product_price = WholesalePurchaseItems.objects.filter(raw_material=product_id).order_by('created').last()
#                 price= product_price.price
#                 print(f"Price from view {i}:", price)
#                 product = get_object_or_404(RawMaterials, pk=product_id)
#                 print(f"Processing row {i} - Product: {product}, Quantity: {quantity}")  # Debugging statement

#                 # Ensure all necessary data for the current row is present
#                 if product and quantity and price:
#                     # Calculate the total cost for the current row
#                     row_total = quantity * price
#                     # Add the row total to the cumulative total cost
#                     total += row_total
#                     print(f"Row {i} total: {row_total}, Cumulative total: {total}")  # Debugging statement

#                     # Create and save a WholesalePurchaseItems object for this row
#                     detail = WholesaleRawMaterialUsage.objects.create(
#                         production_id=production,  # Associate the item with the created production
#                         raw_material=product,
#                         qty=quantity,
#                         unit_cost_price=price,
#                     )
#                     print(f"Saved detail for row {i}:", detail)  # Debugging statement

#             # Optionally, save the total raw material usage cost back to the production object
#             production.total = total
#             production.save()
#             print("Production total saved:", production.total)  # Debugging statement

#             # Return a JSON response indicating success and include the production ID
#             return JsonResponse({"success": True, "production_id": production.production_id})

#         else:
#             # If any required data is missing, print an error and return a JSON response indicating failure
#             print("Error: Missing required production data")
#             return JsonResponse({"success": False, "error": "Missing required production data"})

#     # If the request method is not POST, prepare the context with the empty form and formset for rendering the template
#     context = {
#         "form": form,
#         "formset": formset,
#         "formset2": formset2,
#     }
#     # Render the template for creating a production, passing in the form and formset
#     return render(request, "wholesale/production/create_production.html", context)




# #----- Create Production -------#
# def create_production_out(request):
#     # Initialize the form for the main WholesaleProduction details
#     if request.method == "POST":
#         # Extract individual fields from the POST request data
#         created_at = request.POST.get("created_at")
#         mixture_number = request.POST.get("mixture_number")
#         department = "Wholesale"
#         sub_department_id = request.POST.get("sub_department")
#         session = request.POST.get("session")
#         supervisor = request.POST.get("supervisor")
#         stock_supervisor = request.POST.get("stock_supervisor")

#         # Print the values
#         print("Created At:", created_at)
#         print("Mixture Number:", mixture_number)
#         print("Department:", department)
#         print("Sub Department ID:", sub_department_id)
#         print("Session:", session)
#         print("Supervisor:", supervisor)
#         print("Stock Supervisor:", stock_supervisor)

#         # Fetch the SubDepartment instance based on the provided ID
#         sub_department = get_object_or_404(SubDepartment, pk=sub_department_id)
#         print("Sub Department:", sub_department)

#         # Check if all the required fields are present before creating a WholesaleProduction object
#         if created_at and mixture_number and department and sub_department and session and supervisor and stock_supervisor:
#             # Create a new WholesaleProduction object with the provided data
#             production = WholesaleProduction.objects.create(
#                 created_at=created_at,
#                 mixture_number=mixture_number,
#                 department=department,
#                 sub_department=sub_department,
#                 session=session,
#                 supervisor=supervisor,
#                 stock_supervisor=stock_supervisor
#             )
#             print("Production created:", production)  # Debugging statement to confirm creation
            
#             # Initialize the total raw material usage cost to 0
#             total = 0
#             print("total gotten")  # Debugging statement to confirm total initialization
            
#             # Get the total number of rows of raw material data from the POST request
#             row_count = int(request.POST.get("row_count", 0))
#             print("row gotten: ", row_count)  # Debugging statement to confirm row count retrieval
            
#             # Loop through each row of raw material data submitted
#             for i in range(1, row_count + 1):
#                 print("in for loop")  # Debugging statement to confirm entering the loop
                
#                 # Extract the product ID, quantity, and price from the POST data for each row
#                 output_category= request.POST.get(f"output_category_{i}")
#                 product_id = request.POST.get(f"product_{i}")
#                 quantity = int(request.POST.get(f"quantity_{i}", 0))
                

#                 # Fetch the RawMaterials instance using the extracted product ID
#                 product = get_object_or_404(WholesaleProduct, pk=product_id)
#                 price=product.price
#                 print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, price: {price}")  # Debugging statement

#                 # Ensure all necessary data for the current row is present
#                 if product and quantity and price:
#                     # Calculate the total cost for the current row
#                     row_total = quantity * price
#                     # Add the row total to the cumulative total cost
#                     total += row_total
#                     print(f"Row {i} total: {row_total}, Cumulative total: {total}")  # Debugging statement

#                     # Create and save a WholesalePurchaseItems object for this row
#                     detail = WholesaleProductionOutput.objects.create(
#                         output_category=output_category,
#                         production_id=production,  # Associate the item with the created production
#                         mixture_number=mixture_number,
#                         product=product,
#                         qty=quantity,
#                         product_price=price,
#                         value=total
#                     )
#                     print(f"Saved detail for row {i}:", detail)  # Debugging statement

#             # Optionally, save the total raw material usage cost back to the production object
#             production.total = total
#             production.save()
#             print("Production total saved:", production.total)  # Debugging statement

#             # Return a JSON response indicating success and include the production ID
#             return JsonResponse({"success": True, "production_id": production.production_id})

#         else:
#             # If any required data is missing, print an error and return a JSON response indicating failure
#             print("Error: Missing required production data")
#             return JsonResponse({"success": False, "error": "Missing required production data"})



# def add_more_row_production(request):
#     # Initialize a formset for additional rows, with a prefix to differentiate them
#     formset = WholesaleRawMaterialUsageFormSet(prefix='form')
#     # Get an empty form from the formset to be rendered as a new row
#     empty_form = formset.empty_form
#     # Render the empty form to a string using a specific template for adding a new row
#     rendered_row = render_to_string('wholesale/production/new_row_production.html', {'form': empty_form})
#     # Return a JSON response containing the HTML of the new row to be added dynamically in the frontend
#     return JsonResponse({'row_html': rendered_row})

# #--------------------------- / Production --------------------------------#




#--------------------------------------------------------#
# Detail view of inventories

# @login_required
# def inventory_view(request):
#     inventory = WholesaleInventory.objects.all()

#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')

#     #if start_date:
#         #inventory = inventory.filter(created__range=[start_date, end_date])
#         #total_invoice_amount = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('invoice_total')).values())[0]

#     #else:
#         #inventory = inventory
#         #total_invoice_amount = list(invoices.aggregate(Sum('invoice_total')).values())[0]

#     template_name = 'wholesale/inventory/inventory.html'
#     context = {
#                 'inventory':inventory,
#                 #'total_invoice_amount':total_invoice_amount,
#                 }
#     return render(request, template_name, context)

# class WholesaleInventoryDetailView(DetailView):
#     model = WholesaleInventory
#     template_name = 'wholesale/inventory/inventory-detail-template.html'  # Customize this to your actual template path
#     context_object_name = 'inventory'  # The context variable name for the object in the template

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Fetch related inventory items and add them to the context
#         context['inventory_items'] = WholesaleInventoryItems.objects.filter(inventory_id=self.object)
#         return context


'''
@login_required
def inventory_view(request):
    purchases = WholesaleInventory.objects.all()
   

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    # print(purchases)
    if start_date:
        purchases = purchases.filter(created__range=[start_date, end_date])
        #total_invoice_amount = list(purchases.filter(created__range=[start_date, end_date]).aggregate(Sum('total')).values())[0]

    else:
        purchases = purchases
        #total_invoice_amount = list(purchases.aggregate(Sum('total')).values())[0]
    inventories_with_items = []
    inventories = WholesaleInventory.objects.all()
    #for inventory in inventories:
    #    for item in inventory.wholesaleinventoryitems_set.all():
    #        print(item)
    #        inventories_with_items.append({
    #            'created': inventory.created,
    #            'inventory_id': inventory.inventory_id,
    #            'raw_material_name': item.raw_material_name,
    #            'quantity': item.quantity,
    #            'price': item.price,
    #            'total': item.total,
    #            'status': item.status,
    #        })
    template_name = 'wholesale/inventory/inventory.html'
    context = {
                'inventories_with_items':inventories_with_items,
                #'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)
 '''
# #--------------------------------------------------------#
# def create_inventory(request):
#     form = WholesaleInventoryForm()
#     formset = WholesaleInventoryItemsFormSet(queryset=WholesaleInventoryItems.objects.none())
#     if request.method == "POST":
#         # Extract the main form data from the POST request
#         employee = request.POST.get("employee")
#         created = request.POST.get("created")
        

#         # Print the extracted values
#         print(f"employee: {employee}")
#         print(f"created: {created}")
      

#         # Fetch the customer instance
#         #customer = get_object_or_404(WholesaleCustomer, pk=customer_id)

#         # Print the customer instance to verify it's fetched correctly
        

#         # Create the invoice object
#         if employee and created:
#             invoice = WholesaleInventory.objects.create(
#                 created=created,  # Assign the customer instance here
#                 employee=employee,
#             )
#             print("Invoice created:", invoice)

#             # Initialize total
#             total = 0
#             print("total gotten")
#             # Process each row of invoice details
#             row_count = int(request.POST.get("row_count", 0))  # Number of rows
#             print("row gotten: ", row_count)
#             for i in range(1, row_count + 1):
#                 print("in for loop")
#                 product_id = request.POST.get(f"product_{i}")
#                 print("p id",product_id)
#                 quantity = int(request.POST.get(f"quantity_{i}", 0))
#                 price = float(request.POST.get(f"price_{i}", 0))
#                 status = request.POST.get(f"status_{i}", 0)
                
#                 product = get_object_or_404(RawMaterials, pk=product_id)
#                 print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},status: {status}")

#                 if  product and quantity and price:
#                     # Calculate the sum for each row
#                     row_total = float(price) * float(quantity)
#                     total += row_total  # Add to the total invoice amount
#                     print(f"Row {i} total: {row_total}, Cumulative total: {total}")

#                     # Create and save the WholesaleInvoiceDetail
#                     detail = WholesaleInventoryItems.objects.create(
#                         inventory_id=invoice,
#                         raw_material_name=product,
#                         quantity=quantity,
#                         price=price,
#                         status=status,
#                     )
#                     print(f"Saved detail for row {i}:", detail)

#             # Save the total invoice amount
#             invoice.total_cost = total
#             invoice.save()
#             print("Invoice total saved:", invoice.total_cost)

#             # Optionally, return a JSON response indicating success
#             return JsonResponse({"success": True, "invoice_id": invoice.id})

#         else:
#             print("Error: Missing required invoice data")
#             return JsonResponse({"success": False, "error": "Missing required invoice data"})

#     # Handle GET requests or return an empty form for non-POST requests
#     context = {
#         "form": form,
#         'formset': formset,
#         }
#     return render(request, "wholesale/inventory/create_inventory.html", context)



####FOR AJAX WholesaleInvoice Create
def get_customer_name(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.GET.get('product_id')
        print(product_id)
        try:
            #product = WholesaleCustomer.objects.get(id=product_id)
            product = get_object_or_404(WholesaleInvoice, pk=product_id)
            print(product)
            customer_name = product.customer.customer_name
            customer_id = product.customer_id
            return JsonResponse({'price': customer_name, 'id':customer_id})
        except WholesaleCustomer.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_product_price(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.GET.get('product_id')
        try:
            product = WholesaleProduct.objects.get(id=product_id)
            return JsonResponse({'price': product.selling_price})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_raw_price(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        rm_id = request.GET.get('rm_id')
        try:
            product = WholesalePurchaseItems.objects.filter(raw_material=rm_id).order_by('created').last()
            return JsonResponse({'price': product.price})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def add_more_row(request):
    formset = WholesaleInvoiceDetailFormSet(prefix='form')
    empty_form = formset.empty_form
    rendered_row = render_to_string('wholesale/invoice/new_row.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})


def add_more_row_purchase(request):
    formset = WholesalePurchaseItemsFormSet(prefix='form')
    empty_form = formset.empty_form
    rendered_row = render_to_string('wholesale/purchases/new_row.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})

# def add_more_row_inventory(request):
#     formset = WholesaleInventoryItemsFormSet(prefix='form')
#     empty_form = formset.empty_form
#     rendered_row = render_to_string('wholesale/inventory/new_row.html', {'form': empty_form})
#     return JsonResponse({'row_html': rendered_row})

# def add_more_row_output(request):
#     formset2 = WholesaleProductionOutputFormset(prefix='form')
#     empty_form = formset2.empty_form
#     rendered_row = render_to_string('wholesale/production/new_row_output.html', {'form': empty_form})
#     return JsonResponse({'row_html': rendered_row})
