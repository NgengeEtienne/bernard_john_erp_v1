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
def boulangerie_view(request):
    # Your homepage logic (e.g., display featured content)
    return render(request, 'boulangerie/boulangerie.html')




class BoulangerieProductListView(ListView):
    model = BoulangerieProduct
    template_name = 'boulangerie/product/list.html'
    context_object_name = 'products'

class BoulangerieProductCreateView(CreateView):
    model = BoulangerieProduct
    template_name = 'boulangerie/product/add.html'
    fields = '__all__'  # or specify the fields you want to include
    success_url = reverse_lazy('boulangerie:product-list')  # Redirect after successful creation

class BoulangerieProductUpdateView(UpdateView):
    model = BoulangerieProduct
    template_name = 'boulangerie/product/add.html'
    fields = '__all__'  # or specify the fields you want to include
    success_url = reverse_lazy('boulangerie:product-list')  # Redirect after successful update




# class ProductRecipeListView(ListView):
#     model = ProductRecipe
#     template_name = 'boulangerie/recipe/list.html'
#     context_object_name = 'product_recipes'

# class ProductRecipeCreateView(CreateView):
#     model = ProductRecipe
#     template_name = 'boulangerie/recipe/add_edit.html'
#     fields = ['product', 'recipe', 'quantity_per_product']

#     def form_valid(self, form):
#         form.save()
#         return redirect('boulangerie:productrecipe-list')


# class ProductRecipeUpdateView(UpdateView):
#     model = ProductRecipe
#     template_name = 'boulangerie/recipe/add_edit.html'
#     fields = ['product', 'recipe', 'quantity_per_product']

#     def form_valid(self, form):
#         form.save()
#         return redirect('boulangerie:productrecipe-list')



# #Raw materials
# from django.shortcuts import redirect
# from django.urls import reverse_lazy
# from django.views.generic import ListView, CreateView, UpdateView
# from .models import RawMaterials

# class RawMaterialsListView(ListView):
#     model = RawMaterials
#     template_name = 'boulangerie/raw_materials/list.html'
#     context_object_name = 'raw_materials'

# class RawMaterialsCreateView(CreateView):
#     model = RawMaterials
#     template_name = 'boulangerie/raw_materials/add_edit.html'
#     fields = '__all__'

#     def form_valid(self, form):
#         form.save()
#         return redirect('boulangerie:raw-materials-list')

# class RawMaterialsUpdateView(UpdateView):
#     model = RawMaterials
#     template_name = 'boulangerie/raw_materials/add_edit.html'
#     fields = '__all__'

#     def form_valid(self, form):
#         form.save()
#         return redirect('boulangerie:raw-materials-list')


# #ecipe raw materials
# from django.views.generic import ListView, CreateView, UpdateView
# from .models import RecipeRawMaterial

# class RecipeRawMaterialListView(ListView):
#     model = RecipeRawMaterial
#     template_name = 'boulangerie/reciperawmaterials/list.html'
#     context_object_name = 'boulangerie:recipe_raw_materials'

# class RecipeRawMaterialCreateView(CreateView):
#     model = RecipeRawMaterial
#     template_name = 'boulangerie/reciperawmaterials/add_edit.html'
#     fields = ['recipe', 'raw_material', 'quantity_per_recipe', 'measure']

#     def form_valid(self, form):
#         form.save()
#         return redirect('boulangerie:reciperawmaterial-list')


# class RecipeRawMaterialUpdateView(UpdateView):
#     model = RecipeRawMaterial
#     template_name = 'boulangerie/reciperawmaterials/add_edit.html'
#     fields = ['recipe', 'raw_material', 'quantity_per_recipe', 'measure']

#     def form_valid(self, form):
#         form.save()
#         return redirect('boulangerie:reciperawmaterial-list')

#############   #############   #############   #############   #############
#------------------------- Customer Views ------------------------------#
#############   #############   #############   #############   #############
class BoulangerieCustomerListView(ListView):
    model = BoulangerieCustomer
    template_name = 'boulangerie/boulangerie_customer/customers.html'  # Specify your template name
    context_object_name = 'customers'  # The name to use in the template
    paginate_by = 1000  # Number of customers per page

    def get_queryset(self):
        return BoulangerieCustomer.objects.all().order_by('customer_name')  # Order by customer name

    
class BoulangerieCustomerDetailView(DetailView):
    model = BoulangerieCustomer
    template_name = 'boulangerie/boulangerie_customer/customer_account.html'  # Specify your template name
    context_object_name = 'customer'  # The name to use in the template
    slug_field = 'slug'  # Use slug field for URL lookup
    slug_url_kwarg = 'slug'  # The name of the slug URL parameter

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(BoulangerieCustomer, slug=slug)
    
class BoulangerieCustomerCreateView(View):
    def get(self, request):
        form = BoulangerieCustomerForm()
        return render(request, 'boulangerie/boulangerie_customer/add_customer_form.html', {'form': form})

    def post(self, request):
        form = BoulangerieCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('boulangerie:customer')  # Redirect to customer list after successful creation
        return render(request, 'boulangerie/boulangerie_customer/add_customer_form.html', {'form': form})  
    
class BoulangerieCustomerEditView(UpdateView):
    model = BoulangerieCustomer
    form_class = BoulangerieCustomerForm
    template_name = 'boulangerie/boulangerie_customer/edit_customer_form.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(BoulangerieCustomer, slug=slug)

    def form_valid(self, form):
        form.save()
        return redirect('boulangerie:customer')  # Redirect to the customer list after saving    
    
#############   #############   #############   #############   #############
#------------------------- Product Views ------------------------------#
#############   #############   #############   #############   ############# 
class BoulangerieProductCategoryListView(ListView):
    model = BoulangerieProductSubCategory
    template_name = 'boulangerie/boulangerie_product/categories.html'  # Specify your template name
    context_object_name = 'categories'  # The name to use in the template
    paginate_by = 10  # Number of categories per page

    def get_queryset(self):
        return BoulangerieProductSubCategory.objects.all().order_by('sub_category_name')  # Order by category name


class BoulangerieProductCategoryDetailView(DetailView):
    model = BoulangerieProductSubCategory
    template_name = 'boulangerie/boulangerie_product/category_detail.html'  # Specify your template name
    context_object_name = 'category'  # The name to use in the template
    slug_field = 'slug'  # Use slug field for URL lookup
    slug_url_kwarg = 'slug'  # The name of the slug URL parameter


class BoulangerieProductCategoryCreateView(CreateView):
    model = BoulangerieProductSubCategory
    form_class = BoulangerieProductCategoryForm  # Ensure you have a form for this model
    template_name = 'boulangerie/boulangerie_product/add_category_form.html'  # Specify your template name

    def form_valid(self, form):
        form.save()
        return redirect('boulangerie:category-list')  # Redirect to category list after successful creation
    


class BoulangerieProductCategoryEditView(UpdateView):
    model = BoulangerieProductSubCategory
    form_class = BoulangerieProductCategoryForm
    template_name = 'boulangerie/boulangerie_product/edit_category_form.html'  # Specify your template name

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(BoulangerieProductSubCategory, pk=pk)

    def form_valid(self, form):
        form.save()
        return redirect('boulangerie:category-list')  # Redirect to the category list after saving

#Customer opening

class BoulangerieCustomerOpeningBalanceListView(ListView):
    model = BoulangerieOpeningBalance
    template_name = 'boulangerie/customer_opening_balance/list.html'
    context_object_name = 'customer_opening_balances'

class BoulangerieCustomerOpeningBalanceCreateView(CreateView):
    model = BoulangerieOpeningBalance
    template_name = 'boulangerie/customer_opening_balance/add_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('boulangerie:customer-opening-balance-list')

class BoulangerieCustomerOpeningBalanceUpdateView(UpdateView):
    model = BoulangerieOpeningBalance
    template_name = 'boulangerie/customer_opening_balance/add_edit.html'
    fields ='__all__'
    success_url = reverse_lazy('boulangerie:customer-opening-balance-list')


# class BoulangerieReturnsItemsListView(ListView):
#     model = BoulangerieReturnsItems
#     template_name = 'boulangerie/invoice/returns-list.html'
#     context_object_name = 'return_items'

#     def get_queryset(self):
#         # Ensure that related `customer` objects are properly fetched
#         return super().get_queryset().select_related('customer')

# # class BoulangerieReturnsItemsCreateView(CreateView):
# #     model = BoulangerieReturnsItems
# #     template_name = 'boulangerie/customer_return_items_form.html'
# #     fields = ['date', 'customer', 'invoice', 'product', 'quantity', 'price', 'total']
# #     success_url = reverse_lazy('boulangerie:customer-return-items-list')

# class BoulangerieReturnsItemsUpdateView(UpdateView):
#     model = BoulangerieReturnsItems
#     template_name = 'boulangerie/invoice/edit-returns.html'
#     fields = ['date', 'customer', 'invoice', 'product', 'quantity', 'price', 'total']
#     success_url = reverse_lazy('boulangerie:customer-return-items-list')

# #--------------------------------------------------------#

# Create your views here.
def invoice_view(request):
    invoices = BoulangerieInvoice.objects.all()
    invoices = invoices.annotate(discount=Sum('boulangerieinvoicedetail__discount_value'))
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        invoices = invoices.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('invoice_total')).values())[0]

    else:
        invoices = invoices
        total_invoice_amount = list(invoices.aggregate(Sum('invoice_total')).values())[0]

    template_name = 'boulangerie/invoice/invoices.html'
    context = {
                'invoices':invoices,
                'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)

# Detail view of invoices
def invoice_detail(request, pk):

    invoice = BoulangerieInvoice.objects.get(id=pk)
    invoice_detail = BoulangerieInvoiceDetail.objects.filter(invoice=invoice)

    items = invoice.boulangerieinvoicedetail_set.all()
    items_total = list(items.aggregate(Sum('total_selling_price')).values())[0]

    invoice_payments = invoice.boulangerieinvoicepayment_set.all()
    total_payments = list(invoice_payments.aggregate(Sum('amount_paid')).values())[0]
    payment_installment_count = invoice_payments.count()

    # return_items = invoice.boulangeriereturnsitems_set.all()
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

    return render(request, "boulangerie/invoice/invoice-template.html", context)

from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta, date
def create_invoice(request):
    form = BoulangerieInvoiceForm()
    formset = BoulangerieInvoiceDetailFormSet()
    if request.method == "POST":
        
        supplier_id=int(request.POST.get("customer"))
        created=request.POST.get("created")
        
        status = request.POST.get("status")
        print(f"supplier_id (after conversion): {supplier_id}")
        # print(f"department (after conversion): {department}")
        supplier = get_object_or_404(BoulangerieCustomer, pk=supplier_id)
        print(f"supplier_id: {supplier}")
        print(f"created: {created}")
        # print(f"department: {department}")
        print(f"status: {status}")
        print(f"supplier: {supplier} ")

        if supplier and status and created:
            invoice = BoulangerieInvoice.objects.create(
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

                product = get_object_or_404(BoulangerieProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},Discount amount: {discount_price}")

                if  product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    # Create and save the BoulangerieInvoiceDetail
                    detail = BoulangerieInvoiceDetail.objects.create(
                        invoice=invoice,
                        product=product,
                        quantity=quantity,
                        unit_cost_price=price,
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
    form = BoulangerieInvoiceForm()
    context = {
        "form": form,
        'formset': formset,
        }
    return render(request, "boulangerie/invoice/create_invoice.html", context)




from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

def edit_invoice(request, pk):
    # Fetch the existing invoice using the provided primary key (pk)
    invoice = get_object_or_404(BoulangerieInvoice, id=pk)
    
    # Fetch the associated invoice details
    invoice_details = BoulangerieInvoiceDetail.objects.filter(invoice=invoice)
    
    if request.method == "POST":
        # Extract data from the POST request
        supplier_id = int(request.POST.get("customer"))
        created = request.POST.get("created")
        status = request.POST.get("status")
        
        # Print extracted values for debugging
        print(f"supplier_id (after conversion): {supplier_id}")
        print(f"created: {created}")
        print(f"status: {status}")

        # Fetch the supplier instance
        supplier = get_object_or_404(BoulangerieCustomer, pk=supplier_id)
        print(f"supplier: {supplier}")

        # Update the invoice object
        if supplier and status and created:
            invoice.customer = supplier
            invoice.created = created
            invoice.status = status
            invoice.save()
            print("Invoice updated:", invoice)

            # Process each row of invoice details
            total = 0
            print("total initialized")
            
            row_count = int(request.POST.get("row_count", 0))  # Number of rows
            print("row count: ", row_count)
            for i in range(1, row_count + 1):
                # detail = invoice_details.get(pk=i) if invoice_details.exists() else None
                print("Processing row:", i)
                product_id = request.POST.get(f"product_{i}")
                quantity = int(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                discount_price = float(request.POST.get(f"discount_amount_{i}", 0))
                delivery_man = request.POST.get(f"delivery_man_{i}")

                product = get_object_or_404(BoulangerieProduct, pk=product_id)
                price=product.selling_price
                print(f"Product: {product}, Quantity: {quantity}, Price: {price}, Discount: {discount_price}")

                if product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")
                    if i <= len(invoice_details):
                        detail = invoice_details[i-1]  # Update existing detail
                        detail.product = product
                        detail.quantity = quantity
                        detail.unit_cost_price = price
                        detail.discount_price = discount_price
                        detail.delivery_man = delivery_man
                        detail.save()
                        print(f"Updated detail for row {i}: {detail}")
                    else:
                        # If there are fewer details than rows, create new ones
                        detail = BoulangerieInvoiceDetail.objects.create(
                            invoice=invoice,
                            product=product,
                            quantity=quantity,
                            unit_cost_price=price,
                            discount_price=discount_price,
                            delivery_man=delivery_man
                        )
                        print(f"Created new detail for row {i}: {detail}")

                    # Update or create the BoulangerieInvoiceDetail
                    # detail, created = BoulangerieInvoiceDetail.objects.update_or_create(
                    #     invoice=invoice,
                    #     product=product,
                    #     defaults={
                    #         'quantity': quantity,
                    #         'unit_cost_price': price,
                    #         'discount_price': discount_price,
                    #         'delivery_man': delivery_man
                    #     }
                    # )
                    # print(f"Saved detail for row {i}:", detail)

            # Save the total invoice amount
            invoice.invoice_total = total
            invoice.save()
            print("Invoice total updated:", invoice.invoice_total)

            # Optionally, return a JSON response indicating success
            return JsonResponse({"success": True, "invoice_id": invoice.id})

        else:
            print("Error: Missing required invoice data")
            return JsonResponse({"success": False, "error": "Missing required invoice data"})

    # Handle GET requests or return the form pre-filled with the existing invoice details
    form = BoulangerieInvoiceForm(instance=invoice)
    
    # Prepare the formset with the existing details
    formset_data = [{'product': detail.product.id, 'quantity': detail.quantity, 'unit_selling_price': detail.unit_selling_price, 'discount_price': detail.discount_price}
                    for detail in invoice_details]
    initial_data = [{'product': detail.product, 'quantity': detail.quantity, 'unit_selling_price': detail.unit_selling_price, 'discount_price': detail.discount_price}
                        for detail in invoice_details]
    BoulangerieInvoiceDetailFormSet = modelformset_factory(
    BoulangerieInvoiceDetail,
    form=BoulangerieInvoiceDetailForm,
    extra=0  # No extra forms, handled in the view or template
    )
    # You might need a custom formset initialization to handle editing the details
    formset = BoulangerieInvoiceDetailFormSet(queryset=invoice_details, initial=initial_data)
    print(type(invoice_details))  # Should be <class 'django.db.models.query.QuerySet'>

    context = {
        "form": form,
        'formset': formset,
        "invoice": invoice,  # Pass the invoice to the template if needed
    }
    return render(request, "boulangerie/invoice/edit_invoice.html", context)



#--------------------------------------------------------------------#

# Invoice view
def InvoicePayment_view(request):
        invoice = BoulangerieInvoice.objects.all()
        customer = Customer.objects.all()
        invoice_payment = BoulangerieInvoicePayment.objects.all().order_by('-date')
        #invoice_grand_total = list(invoices.aggregate(Sum('grand_total')).values())[0]

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date:
            invoice_payment = invoice_payment.filter(created__range=[start_date, end_date])
        else:
            invoice_payment = BoulangerieInvoicePayment.objects.all().order_by('-date')
            #total_orders = list(invoices.aggregate(Sum('amount')).values())[0]
        for payment in invoice_payment:
            print("Invoice payment:", payment.invoice)
        template_name = 'boulangerie/invoice/invoice_payments.html'
        context = {
                    'invoice_payment':invoice_payment,
                    "invoice":invoice,
                    "customer":customer ,

                    }
        return render(request, template_name, context)

class add_payment_view(SuccessMessageMixin, CreateView):
        model = BoulangerieInvoicePayment
        template_name = 'boulangerie/invoice/add_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("boulangerie:invoice-payments")
        success_message = 'Payment Transaction successful'

# Invoice view
class edit_payment_view(SuccessMessageMixin, UpdateView):
        model = BoulangerieInvoicePayment
        template_name = 'boulangerie/invoice/edit_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("boulangerie:invoice-payments")
        success_message = 'Payment Transaction successfully Updated'

        # def get_object(self, queryset=None):
        #         # Get the payment by id (pk) from the URL
        #         payment_id = self.kwargs.get('pk')
        #         # Store the payment in a variable
        #         payment = BoulangerieInvoicePayment.objects.get(id=payment_id)
        #         print(payment)
        #         return payment

        # def get_context_data(self, **kwargs):
        #     # Call the base implementation to get the context
        #     context = super().get_context_data(**kwargs)
        #     # Add the payment object to the context
        #     context['payment'] = self.get_object()
        #     return context
# class add_returns_view(SuccessMessageMixin, CreateView):
#         model = BoulangerieReturnsItems
#         template_name = 'boulangerie/invoice/add_returns.html'
#         fields = '__all__'
#         #exclude = ('slug',)
#         success_url = reverse_lazy('boulangerie:invoice-payments')
#         success_message = 'Payment Transaction successful'



########################PURCHASES##############
# Create your views here.
@login_required
def purchases_view(request):
    purchases = BoulangeriePurchase.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    print(purchases)
    if start_date:
        purchases = purchases.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(purchases.filter(created__range=[start_date, end_date]).aggregate(Sum('purchase_total')).values())[0]

    else:
        purchases = purchases
        total_invoice_amount = list(purchases.aggregate(Sum('purchase_total')).values())[0]

    template_name = 'boulangerie/purchases/purchase_invoices.html'
    context = {
                'purchases':purchases,
                'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)
 
    #--------------------------------------------------------#
    # Detail view of invoices
@login_required
def purchase_detail(request, pk):

    invoice = BoulangeriePurchase.objects.get(id=pk)
    purchases_detail = BoulangeriePurchaseItems.objects.filter(purchase_id=invoice)

    #items = invoice.invoicedetail_set.all()
    #items_total = list(items.aggregate(Sum('total')).values())[0]

    # purchase_invoice_payments = invoice.purchaseinvoicespayment_set.all()
    # total_payments = list(purchase_invoice_payments.aggregate(Sum('amount_paid')).values())[0]
    # #payment_installment_count = invoice_payments.count()
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

    return render(request, "boulangerie/purchases/purchases-invoice-template.html", context)
#---------------------------------------------------------------------------------------#
# BoulangerieInvoice view
@login_required
def create_purchase(request):

    form = BoulangeriePurchaseForm()
    formset = BoulangeriePurchaseItemsFormSet(queryset=BoulangeriePurchase.objects.none())
    if request.method == "POST":
        
        supplier_id=int(request.POST.get("supplier_name"))
        created=request.POST.get("created")
        employee = request.POST.get("employee")
        status = request.POST.get("status")
        print(f"supplier_id (after conversion): {supplier_id}")
        # print(f"department (after conversion): {department}")
        # supplier = BoulangerieSupplier.objects.filter(id=supplier_id)
        supplier = BoulangerieSupplier.objects.get(id=supplier_id)

        print(f"supplier_id: {supplier}")
        print(f"created: {created}")
        # print(f"department: {department}")
        print(f"sales_session: {employee}")
        print(f"supplier: {supplier} ")
 
        if supplier and employee and created:
            invoice = BoulangeriePurchase.objects.create(
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

                product = get_object_or_404(BoulangerieProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},Discount amount: {discount_price}")

                if  product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    # Create and save the BoulangerieInvoiceDetail
                    detail = BoulangeriePurchaseItems.objects.create(
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

        #return redirect("boulangerie:purchases")

    context = {

        #"total_invoice": total_invoice,
        "form": form,
        "formset": formset,
    }

    return render(request, "boulangerie/purchases/create_purchase.html", context)
#--------------------------------------------------------------------#


@login_required
def edit_purchase(request, pk):
    # Fetch the existing invoice and its items
    invoice = get_object_or_404(BoulangeriePurchase, pk=pk)
    invoice_items = BoulangeriePurchaseItems.objects.filter(purchase_id=invoice)
    BarPurchaseItemsFormSet = modelformset_factory(BoulangeriePurchaseItems, form=BoulangeriePurchaseItemsForm, extra=0, can_delete=True)

    # Initialize the forms with existing invoice data
    form = BoulangeriePurchaseForm(instance=invoice)
    formset = BarPurchaseItemsFormSet(queryset=invoice_items)

    if request.method == "POST":
        # Extract the main form data from the POST request
        supplier_id = int(request.POST.get("supplier_name"))
        created = request.POST.get("created")
        employee = request.POST.get("employee")
        status = request.POST.get("status")

        # Fetch the supplier instance
        supplier = get_object_or_404(BoulangerieSupplier, pk=supplier_id)

        # Ensure all necessary fields are provided
        if supplier and employee and created:
            # Update the invoice object
            invoice.supplier_name = supplier
            invoice.created = created
            invoice.status = status
            invoice.employee = employee
            invoice.save()
            print("Invoice updated:", invoice)

            # Initialize the total
            total = 0

            # Process each row of invoice details
            row_count = int(request.POST.get("row_count", 0))  # Number of rows
            print("Row count:", row_count)
            
            for i in range(1, row_count + 1):
                product_id = request.POST.get(f"product_{i}")
                quantity = int(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                discount_price = float(request.POST.get(f"discount_amount_{i}", 0))

                # Fetch the product instance
                product = get_object_or_404(BoulangerieProduct, pk=product_id)

                if product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    if i <= len(invoice_items):
                        # Update existing detail
                        detail = invoice_items[i - 1]
                        detail.product = product
                        detail.quantity = quantity
                        detail.price = price
                        detail.discount_amount = discount_price
                        detail.save()
                        print(f"Updated detail for row {i}: {detail}")
                    else:
                        # Create new detail if fewer details than rows
                        detail = BoulangeriePurchaseItems.objects.create(
                            purchase_id=invoice,
                            product=product,
                            quantity=quantity,
                            price=price,
                            discount_amount=discount_price
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

    return render(request, "boulangerie/purchases/create_purchase.html", context)


# BoulangerieInvoice view
@login_required
def purchase_invoice_payments_view(request):
        invoice = BoulangerieInvoice.objects.all()
        supplier = BoulangerieSupplier.objects.all()
        purchase_invoice_payment = BoulangerieInvoicePayment.objects.all().order_by('-date')
        #invoice_grand_total = list(invoices.aggregate(Sum('grand_total')).values())[0]

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date:
            purchase_invoice_payment = purchase_invoice_payment.filter(created__range=[start_date, end_date])
            #total_orders = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('amount')).values())[0]

        else:
            purchase_invoice_payment = purchase_invoice_payment
            #total_orders = list(invoices.aggregate(Sum('amount')).values())[0]

        template_name = 'boulangerie/purchases/purchase_invoice_payments.html'
        context = {
                    'purchase_invoice_payment':purchase_invoice_payment,
                    "invoice":invoice,
                    "supplier":supplier ,

                    }
        return render(request, template_name, context)
    
class add_purchase_payment_view(SuccessMessageMixin, CreateView):
        model = BoulangerieInvoicePayment
        template_name = 'boulangerie/purchases/add_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("boulangerie:purchases")
        success_message = 'Payment Transaction successful'

# BoulangerieInvoice view
class edit_purchase_payment_view(SuccessMessageMixin, UpdateView):
        model = BoulangerieInvoicePayment
        template_name = 'boulangerie/purchases/edit_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("boulangerie:purchases")
        success_message = 'Payment Transaction successfully Updated'







###################################SUPPLIER############################

# Create your views here.
@login_required
def suppliers_view(request):
    suppliers = BoulangerieSupplier.objects.all()

    template_name = 'boulangerie/supplier/suppliers.html'
    context = {'suppliers':suppliers}
    return render(request, template_name, context)
#-------------------------------------------------------------------#
@login_required
def supplier_details(request, id):#
    supplier = get_object_or_404(BoulangerieSupplier, id=id)
    supplier_invoice = supplier.boulangeriepurchase_set.filter(status='Purchases')
    supplier_invoice_total = list(supplier_invoice.aggregate(Sum('purchase_total')).values())[0]

    purchase_returns = supplier.boulangeriepurchase_set.filter(status='Return Outwards')
    total_purchase_returns= list(purchase_returns.aggregate(Sum('purchase_total')).values())[0]

    if supplier_invoice_total is not None and total_purchase_returns is not None:
        account_balance = supplier_invoice_total - total_purchase_returns
    else:
        account_balance = 0.00

    template_name = 'bar/supplier/supplier_account.html'
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
    model = BoulangerieSupplier
    template_name = 'boulangerie/supplier/forms/add_supplier.html'
    fields = '__all__'
    exclude = ('slug',)
    success_url = reverse_lazy('boulangerie:supplier')
    success_message = 'supplier Account Successfully Created !!!'

#-------------------------------------------------------------------------#
class edit_supplier(SuccessMessageMixin, UpdateView):
    model = BoulangerieSupplier
    template_name = 'boulangerie/supplier/forms/edit_supplier.html'
    fields = '__all__'
    exclude = ('slug',)
    success_url = reverse_lazy('boulangerie:supplier')
    success_message = 'supplier Account Successfully Edited !!!'
#-------------------------------------------------------------------------#




#--------------------------------------------------------#
# Detail view of inventories
 
@login_required
def inventory_view(request):
    inventory = BoulangerieInventory.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        inventory = inventory.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(inventory.filter(created__range=[start_date, end_date]).aggregate(Sum('total_price')).values())[0]

    else:
        inventory = inventory
        total_invoice_amount = list(inventory.aggregate(Sum('total_price')).values())[0]
    print(total_invoice_amount)
    template_name = 'boulangerie/inventory/inventory.html'
    context = {
                'inventory':inventory,
                'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)

class BoulangerieInventoryDetailView(DetailView):
    model = BoulangerieInventory
    template_name = 'boulangerie/inventory/inventory-detail-template.html'  # Customize this to your actual template path
    context_object_name = 'inventory'  # The context variable name for the object in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch related inventory items and add them to the context
        context['inventory_items'] = BoulangerieInventoryItems.objects.filter(inventory_id=self.object)
        return context


'''
@login_required
def inventory_view(request):
    purchases = BoulangerieInventory.objects.all()
   

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
    inventories = BoulangerieInventory.objects.all()
    #for inventory in inventories:
    #    for item in inventory.boulangerieinventoryitems_set.all():
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
    template_name = 'boulangerie/inventory/inventory.html'
    context = {
                'inventories_with_items':inventories_with_items,
                #'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)
 '''
#--------------------------------------------------------#
def create_inventory(request):
    form = BoulangerieInventoryForm()
    formset = BoulangerieInventoryItemsFormSet(queryset=BoulangerieInventoryItems.objects.none())
    if request.method == "POST":
        # Extract the main form data from the POST request
        employee = request.POST.get("employee")
        created = request.POST.get("created")
        description = request.POST.get("description")

        # Print the extracted values
        print(f"employee: {employee}")
        print(f"created: {created}")
      

        # Fetch the customer instance
        #customer = get_object_or_404(BoulangerieCustomer, pk=customer_id)

        # Print the customer instance to verify it's fetched correctly
        

        # Create the invoice object
        if employee and created:
            invoice = BoulangerieInventory.objects.create(
                created=created,  # Assign the customer instance here
                employee=employee,
                description=description,
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
                quantity = int(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                status = request.POST.get(f"status_{i}", 0)
                
                product = get_object_or_404(BoulangerieProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},status: {status}")

                if  product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    # Create and save the BoulangerieInvoiceDetail
                    detail = BoulangerieInventoryItems.objects.create(
                        inventory_id=invoice,
                        product_name=product,
                        quantity=quantity,
                        selling_price=price,
                        status=status,
                    )
                    print(f"Saved detail for row {i}:", detail)

            # Save the total invoice amount
            invoice.total_price = total
            invoice.save()
            print("Invoice total saved:", invoice.total_price)

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
    return render(request, "boulangerie/inventory/create_inventory.html", context)

@login_required
def edit_inventory(request, pk):
    # Fetch the existing inventory and its items
    invoice = get_object_or_404(BoulangerieInventory, pk=pk)
    invoice_items = BoulangerieInventoryItems.objects.filter(inventory_id=invoice)
    BarInventoryItemsFormSet = modelformset_factory(BoulangerieInventoryItems, form=BoulangerieInventoryItemsForm, extra=0, can_delete=True)

    # Initialize the forms with existing inventory data
    form = BoulangerieInventoryForm(instance=invoice)
    formset = BarInventoryItemsFormSet(queryset=invoice_items)

    if request.method == "POST":
        # Extract the main form data from the POST request
        employee = request.POST.get("employee")
        created = request.POST.get("created")
        description = request.POST.get("description")
        department=Department.objects.filter(department_name="Boulangerie").first()
        print(f"department: {department}")
        # description = request.POST.get("description")
        # Update the inventory object
        if employee and created:
            invoice.employee = employee
            invoice.created = created
            invoice.description = description
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
                quantity = int(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                status = request.POST.get(f"status_{i}", 0)

                product = get_object_or_404(BoulangerieProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price}, Status: {status}")

                if product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    if i <= len(invoice_items):
                        # Update existing detail
                        detail = invoice_items[i - 1]
                        product_name=product,
                        quantity=quantity,
                        selling_price=price,
                        status=status
                        detail.save()
                        print(f"Updated detail for row {i}: {detail}")
                    else:
                        # Create new detail if there are more rows than existing items
                        detail = BoulangerieInventoryItems.objects.create(
                            inventory_id=invoice,
                            product_name=product,
                            quantity=quantity,
                            selling_price=price,
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

    return render(request, "boulangerie/inventory/create_inventory.html", context)


# #--------------------------- Production --------------------------------#
# #----- Production List -------#
# class BoulangerieProductionListView(ListView):
#     model = BoulangerieProduction
#     template_name = 'boulangerie/production/production_list.html'
#     context_object_name = 'production'

# #----- Create Production -------#
# def create_production(request):
#     # Initialize the form for the main BoulangerieProduction details
#     form = BoulangerieProductionForm()
#     # Initialize the formset for handling multiple raw material usages
#     formset = BoulangerieRawMaterialUsageFormSet(queryset=BoulangerieProduction.objects.none())
#     formset2 = BoulangerieProductionOutputFormset(queryset=BoulangerieProductionOutput.objects.none())

#     # Check if the request is a POST request (form submission)
#     if request.method == "POST":
#         # Extract individual fields from the POST request data
#         created_at = request.POST.get("created_at")
#         mixture_number = request.POST.get("mixture_number")
#         department = "Boulangerie"
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

#         # Check if all the required fields are present before creating a BoulangerieProduction object
#         if created_at and mixture_number and department and sub_department and session and supervisor and stock_supervisor:
#             # Create a new BoulangerieProduction object with the provided data
#             production = BoulangerieProduction.objects.create(
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
#                 product_price = BoulangeriePurchaseItems.objects.filter(raw_material=product_id).order_by('created').last()
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

#                     # Create and save a BoulangeriePurchaseItems object for this row
#                     detail = BoulangerieRawMaterialUsage.objects.create(
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
#     return render(request, "boulangerie/production/create_production.html", context)




# #----- Create Production -------#
# def create_production_out(request):
#     # Initialize the form for the main BoulangerieProduction details
#     if request.method == "POST":
#         # Extract individual fields from the POST request data
#         created_at = request.POST.get("created_at")
#         mixture_number = request.POST.get("mixture_number")
#         department = "Boulangerie"
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

#         # Check if all the required fields are present before creating a BoulangerieProduction object
#         if created_at and mixture_number and department and sub_department and session and supervisor and stock_supervisor:
#             # Create a new BoulangerieProduction object with the provided data
#             production = BoulangerieProduction.objects.create(
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
#                 product = get_object_or_404(BoulangerieProduct, pk=product_id)
#                 price=product.price
#                 print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, price: {price}")  # Debugging statement

#                 # Ensure all necessary data for the current row is present
#                 if product and quantity and price:
#                     # Calculate the total cost for the current row
#                     row_total = quantity * price
#                     # Add the row total to the cumulative total cost
#                     total += row_total
#                     print(f"Row {i} total: {row_total}, Cumulative total: {total}")  # Debugging statement

#                     # Create and save a BoulangeriePurchaseItems object for this row
#                     detail = BoulangerieProductionOutput.objects.create(
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
#     formset = BoulangerieRawMaterialUsageFormSet(prefix='form')
#     # Get an empty form from the formset to be rendered as a new row
#     empty_form = formset.empty_form
#     # Render the empty form to a string using a specific template for adding a new row
#     rendered_row = render_to_string('boulangerie/production/new_row_production.html', {'form': empty_form})
#     # Return a JSON response containing the HTML of the new row to be added dynamically in the frontend
#     return JsonResponse({'row_html': rendered_row})

# #--------------------------- / Production --------------------------------#




#--------------------------------------------------------#
# Detail view of inventories

# @login_required
# def inventory_view(request):
#     inventory = BoulangerieInventory.objects.all()

#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')

#     #if start_date:
#         #inventory = inventory.filter(created__range=[start_date, end_date])
#         #total_invoice_amount = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('invoice_total')).values())[0]

#     #else:
#         #inventory = inventory
#         #total_invoice_amount = list(invoices.aggregate(Sum('invoice_total')).values())[0]

#     template_name = 'boulangerie/inventory/inventory.html'
#     context = {
#                 'inventory':inventory,
#                 #'total_invoice_amount':total_invoice_amount,
#                 }
#     return render(request, template_name, context)

# class BoulangerieInventoryDetailView(DetailView):
#     model = BoulangerieInventory
#     template_name = 'boulangerie/inventory/inventory-detail-template.html'  # Customize this to your actual template path
#     context_object_name = 'inventory'  # The context variable name for the object in the template

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Fetch related inventory items and add them to the context
#         context['inventory_items'] = BoulangerieInventoryItems.objects.filter(inventory_id=self.object)
#         return context


'''
@login_required
def inventory_view(request):
    purchases = BoulangerieInventory.objects.all()
   

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
    inventories = BoulangerieInventory.objects.all()
    #for inventory in inventories:
    #    for item in inventory.boulangerieinventoryitems_set.all():
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
    template_name = 'boulangerie/inventory/inventory.html'
    context = {
                'inventories_with_items':inventories_with_items,
                #'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)
 '''
# #--------------------------------------------------------#
# def create_inventory(request):
#     form = BoulangerieInventoryForm()
#     formset = BoulangerieInventoryItemsFormSet(queryset=BoulangerieInventoryItems.objects.none())
#     if request.method == "POST":
#         # Extract the main form data from the POST request
#         employee = request.POST.get("employee")
#         created = request.POST.get("created")
        

#         # Print the extracted values
#         print(f"employee: {employee}")
#         print(f"created: {created}")
      

#         # Fetch the customer instance
#         #customer = get_object_or_404(BoulangerieCustomer, pk=customer_id)

#         # Print the customer instance to verify it's fetched correctly
        

#         # Create the invoice object
#         if employee and created:
#             invoice = BoulangerieInventory.objects.create(
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

#                     # Create and save the BoulangerieInvoiceDetail
#                     detail = BoulangerieInventoryItems.objects.create(
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
#     return render(request, "boulangerie/inventory/create_inventory.html", context)



####FOR AJAX BoulangerieInvoice Create
def get_customer_name(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.GET.get('product_id')
        print(product_id)
        try:
            #product = BoulangerieCustomer.objects.get(id=product_id)
            product = get_object_or_404(BoulangerieInvoice, pk=product_id)
            print(product)
            customer_name = product.customer.customer_name
            customer_id = product.customer_id
            return JsonResponse({'price': customer_name, 'id':customer_id})
        except BoulangerieCustomer.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_product_price(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.GET.get('product_id')
        try:
            product = BoulangerieProduct.objects.get(id=product_id)
            return JsonResponse({'price': product.selling_price})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_raw_price(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        rm_id = request.GET.get('rm_id')
        try:
            product = BoulangeriePurchaseItems.objects.filter(raw_material=rm_id).order_by('created').last()
            return JsonResponse({'price': product.price})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def add_more_row(request):
    formset = BoulangerieInvoiceDetailFormSet(prefix='form')
    empty_form = formset.empty_form
    rendered_row = render_to_string('boulangerie/invoice/new_row.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})


def add_more_row_purchase(request):
    formset = BoulangeriePurchaseItemsFormSet(prefix='form')
    empty_form = formset.empty_form
    rendered_row = render_to_string('boulangerie/purchases/new_row.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})

def add_more_row_inventory(request):
    formset = BoulangerieInventoryItemsFormSet(prefix='form')
    empty_form = formset.empty_form
    rendered_row = render_to_string('boulangerie/inventory/new_row.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})

# def add_more_row_output(request):
#     formset2 = BoulangerieProductionOutputFormset(prefix='form')
#     empty_form = formset2.empty_form
#     rendered_row = render_to_string('boulangerie/production/new_row_output.html', {'form': empty_form})
#     return JsonResponse({'row_html': rendered_row})
