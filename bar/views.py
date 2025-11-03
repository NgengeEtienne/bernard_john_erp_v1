from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
#from .forms import *
from django.db.models import Sum
from django.db.models import Q
from django.utils import timezone
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




class BarProductListView(ListView):
    model = BarProduct
    template_name = 'bar/product/list.html'  # Update this with your actual template path
    context_object_name = 'products'


class BarProductCreateView(CreateView):
    model = BarProduct
    template_name = 'bar/product/add.html'  # Ensure this path is correct
    fields = '__all__'
    success_url = reverse_lazy('bar:product-list')  # Ensure this matches your URL names
    

class BarProductUpdateView(UpdateView):
    model = BarProduct
    template_name = 'bar/product/add.html'
    fields = ['product_name', 'category', 'price', 'selling_price', 'unit_measure']
    success_url = reverse_lazy('bar:product-list')

@login_required
def bar_view(request):
    # Your homepage logic (e.g., display featured content)
    return render(request, 'bar/bar.html')

#############   #############   #############   #############   #############
#------------------------- Customer Views ------------------------------#
#############   #############   #############   #############   #############
# class BarCustomerListView(ListView):
#     model = BarCustomer
#     template_name = 'bar/bar_customer/customers.html'  # Specify your template name
#     context_object_name = 'customers'  # The name to use in the template
#     paginate_by = 1000  # Number of customers per page

#     def get_queryset(self):
#         return BarCustomer.objects.all().order_by('customer_name')  # Order by customer name

    
# class BarCustomerDetailView(DetailView):
#     model = BarCustomer
#     template_name = 'bar/bar_customer/customer_account.html'  # Specify your template name
#     context_object_name = 'customer'  # The name to use in the template
#     slug_field = 'slug'  # Use slug field for URL lookup
#     slug_url_kwarg = 'slug'  # The name of the slug URL parameter

#     def get_object(self, queryset=None):
#         slug = self.kwargs.get('slug')
#         return get_object_or_404(BarCustomer, slug=slug)
    
# class BarCustomerCreateView(View):
#     def get(self, request):
#         form = BarCustomerForm()
#         return render(request, 'bar/bar_customer/add_customer_form.html', {'form': form})

#     def post(self, request):
#         form = BarCustomerForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('bar:customer')  # Redirect to customer list after successful creation
#         return render(request, 'bar/bar_customer/add_customer_form.html', {'form': form})  
    
# class BarCustomerEditView(UpdateView):
#     model = BarCustomer
#     form_class = BarCustomerForm
#     template_name = 'bar/bar_customer/edit_customer_form.html'

#     def get_object(self):
#         slug = self.kwargs.get('slug')
#         return get_object_or_404(BarCustomer, slug=slug)

#     def form_valid(self, form):
#         form.save()
#         return redirect('bar:customer')  # Redirect to the customer list after saving    
    
#############   #############   #############   #############   #############
#------------------------- Product Views ------------------------------#
#############   #############   #############   #############   ############# 
class BarProductCategoryListView(ListView):
    model = BarProductCategory
    template_name = 'bar/bar_product/categories.html'  # Specify your template name
    context_object_name = 'categories'  # The name to use in the template
    paginate_by = 10  # Number of categories per page

    def get_queryset(self):
        return BarProductCategory.objects.all().order_by('category_name')  # Order by category name


class BarProductCategoryDetailView(DetailView):
    model = BarProductCategory
    template_name = 'bar/bar_product/category_detail.html'  # Specify your template name
    context_object_name = 'category'  # The name to use in the template
    slug_field = 'slug'  # Use slug field for URL lookup
    slug_url_kwarg = 'slug'  # The name of the slug URL parameter


class BarProductCategoryCreateView(CreateView):
    model = BarProductCategory
    form_class = BarProductCategoryForm  # Ensure you have a form for this model
    template_name = 'bar/bar_product/add_category_form.html'  # Specify your template name

    def form_valid(self, form):
        form.save()
        return redirect('bar:category-list')  # Redirect to category list after successful creation
    


class BarProductCategoryEditView(UpdateView):
    model = BarProductCategory
    form_class = BarProductCategoryForm
    template_name = 'bar/bar_product/edit_category_form.html'  # Specify your template name

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(BarProductCategory, pk=pk)

    def form_valid(self, form):
        form.save()
        return redirect('bar:category-list')  # Redirect to the category list after saving

   
#--------------------------------------------------------#

# # Create your views here.
# def invoice_view(request):
#     invoices = BarInvoice.objects.all()

#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')

#     if start_date:
#         invoices = invoices.filter(created__range=[start_date, end_date])
#         total_invoice_amount = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('invoice_total')).values())[0]

#     else:
#         invoices = invoices
#         total_invoice_amount = list(invoices.aggregate(Sum('invoice_total')).values())[0]

#     template_name = 'bar/invoice/invoices.html'
#     context = {
#                 'invoices':invoices,
#                 'total_invoice_amount':total_invoice_amount,
#                 }
#     return render(request, template_name, context)

# # Detail view of invoices
# def invoice_detail(request, pk):

#     invoice = BarInvoice.objects.get(id=pk)
#     invoice_detail = BarInvoiceDetail.objects.filter(invoice=invoice)

#     items = invoice.barinvoicedetail_set.all()
#     items_total = list(items.aggregate(Sum('total')).values())[0]

#     invoice_payments = invoice.barinvoicepayment_set.all()
#     total_payments = list(invoice_payments.aggregate(Sum('amount_paid')).values())[0]
#     payment_installment_count = invoice_payments.count()

#     return_items = invoice.barreturnsitems_set.all()
#     total_returns = list(return_items.aggregate(Sum('total')).values())[0]

#     print(invoice)

#     context = {
#         'invoice': invoice,
#         "invoice_detail": invoice_detail,
#         #'items_total':items_total,
#         'invoice_payments':invoice_payments,
#         'total_payments':total_payments,
#         'payment_installment_count':payment_installment_count,

#         "return_items":return_items,
#         'total_returns':total_returns,

#     }

#     return render(request, "bar/invoice/invoice-template.html", context)

# from django.shortcuts import get_object_or_404
# from datetime import datetime, timedelta, date
# def create_invoice(request):
#     form = BarInvoiceForm()
#     formset = BarInvoiceDetailFormSet()
#     if request.method == "POST":
        
#         # Extract the main form data from the POST request
#         customer_id = request.POST.get("customer")
#         created = request.POST.get("created")
#         sales_session = request.POST.get("sales_session")
#         sales_person = request.POST.get("sales_person")

#         # Print the extracted values
#         print(f"customer_id: {customer_id}")
#         print(f"created: {created}")
#         print(f"sales_session: {sales_session}")
#         print(f"sales_person: {sales_person}")
        
        

#         # Fetch the customer instance
#         customer = get_object_or_404(BarCustomer, pk=customer_id)

#         # Print the customer instance to verify it's fetched correctly
#         print(f"customer: {customer}")

#         # Create the invoice object
#         if sales_person and customer and created and sales_session:
#             invoice = BarInvoice.objects.create(
#                 customer=customer,  # Assign the customer instance here
#                 created=created,
#                 sales_session=sales_session,
#                 sales_person=sales_person,
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
#                 quantity = int(request.POST.get(f"quantity_{i}", 0))
#                 price = float(request.POST.get(f"price_{i}", 0))
#                 discount_price = float(request.POST.get(f"discount_price_{i}", 0))

#                 product = get_object_or_404(BarProduct, pk=product_id)
#                 print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},Discount Price: {discount_price}")

#                 if  product and quantity and price:
#                     # Calculate the sum for each row
#                     row_total = float(price) * float(quantity)
#                     total += row_total  # Add to the total invoice amount
#                     print(f"Row {i} total: {row_total}, Cumulative total: {total}")

#                     # Create and save the BarInvoiceDetail
#                     detail = BarInvoiceDetail.objects.create(
#                         invoice=invoice,
#                         product=product,
#                         quantity=quantity,
#                         price=price,
#                         discount_price=discount_price,
#                     )
#                     print(f"Saved detail for row {i}:", detail)

#             # Save the total invoice amount
#             invoice.invoice_total = total
#             invoice.save()
#             print("Invoice total saved:", invoice.invoice_total)

#             # Optionally, return a JSON response indicating success
#             return JsonResponse({"success": True, "invoice_id": invoice.id})

#         else:
#             print("Error: Missing required invoice data")
#             return JsonResponse({"success": False, "error": "Missing required invoice data"})

#     # Handle GET requests or return an empty form for non-POST requests
#     form = BarInvoiceForm()
#     context = {
#         "form": form,
#         'formset': formset,
#         }
#     return render(request, "bar/invoice/create_invoice.html", context)


#--------------------------------------------------------------------#

# # Invoice view
# def InvoicePayment_view(request):
#         invoice = BarInvoice.objects.all()
#         customer = Customer.objects.all()
#         invoice_payment = BarInvoicePayment.objects.all().order_by('-date')
#         #invoice_grand_total = list(invoices.aggregate(Sum('grand_total')).values())[0]

#         start_date = request.GET.get('start_date')
#         end_date = request.GET.get('end_date')

#         if start_date:
#             invoice_payment = invoice_payment.filter(created__range=[start_date, end_date])
#         else:
#             invoice_payment = BarInvoicePayment.objects.all().order_by('-date')
#             #total_orders = list(invoices.aggregate(Sum('amount')).values())[0]
#         for payment in invoice_payment:
#             print("Invoice payment:", payment.invoice)
#         template_name = 'bar/invoice/invoice_payments.html'
#         context = {
#                     'invoice_payment':invoice_payment,
#                     "invoice":invoice,
#                     "customer":customer ,

#                     }
#         return render(request, template_name, context)

# class add_payment_view(SuccessMessageMixin, CreateView):
#         model = BarInvoicePayment
#         template_name = 'bar/invoice/add_payment.html'
#         fields = '__all__'
#         #exclude = ('slug',)
#         success_url = reverse_lazy("bar:invoice-payments")
#         success_message = 'Payment Transaction successful'

# # Invoice view
# class edit_payment_view(SuccessMessageMixin, UpdateView):
#         model = BarInvoicePayment
#         template_name = 'bar/invoice/edit_payment.html'
#         fields = '__all__'
#         #exclude = ('slug',)
#         success_url = reverse_lazy("bar:invoice-payments")
#         success_message = 'Payment Transaction successfully Updated'

# class add_returns_view(SuccessMessageMixin, CreateView):
#         model = BarReturnsItems
#         template_name = 'bar/invoice/add_returns.html'
#         fields = '__all__'
#         #exclude = ('slug',)
#         success_url = reverse_lazy('bar:invoice-payments')
#         success_message = 'Payment Transaction successful'



########################PURCHASES##############
# Create your views here.
@login_required
def purchases_view(request):
    purchases = BarPurchase.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    print(purchases)
    if start_date:
        purchases = purchases.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(purchases.filter(created__range=[start_date, end_date]).aggregate(Sum('purchase_total')).values())[0]

    else:
        purchases = purchases
        total_invoice_amount = list(purchases.aggregate(Sum('purchase_total')).values())[0]

    template_name = 'bar/purchases/purchase_invoices.html'
    context = {
                'purchases':purchases,
                'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)
 
    #--------------------------------------------------------#
    # Detail view of invoices
@login_required
def purchase_detail(request, pk):

    invoice = BarPurchase.objects.get(id=pk)
    purchases_detail = BarPurchaseItems.objects.filter(purchase_id=invoice)

    #items = invoice.invoicedetail_set.all()
    #items_total = list(items.aggregate(Sum('total')).values())[0]

    # purchase_invoice_payments = invoice.purchaseinvoicespayment_set.all()
    # total_payments = list(purchase_invoice_payments.aggregate(Sum('amount_paid')).values())[0]
    #payment_installment_count = invoice_payments.count()
    # print(total_payments)
    #return_items = invoice.returnsitems_set.all()
    #total_returns = list(return_items.aggregate(Sum('total')).values())[0]
    for i in purchases_detail:
        print(i.pk)

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

    return render(request, "bar/purchases/purchases-invoice-template.html", context)
#---------------------------------------------------------------------------------------#
# BarInvoice view
@login_required
def create_purchase(request):

    form = BarPurchaseForm()
    formset = BarPurchaseItemsFormSet(queryset=BarPurchase.objects.none())
    if request.method == "POST":
        
        supplier_id=int(request.POST.get("supplier_name"))
        created=request.POST.get("created")
        status=request.POST.get("status")
        department=request.POST.get("sub_department")
        employee = request.POST.get("employee")
        print(f"supplier_id (after conversion): {supplier_id}")
        # print(f"department (after conversion): {department}")
        supplier = get_object_or_404(BarSupplier, pk=supplier_id)
        print(f"supplier_id: {supplier}")
        # print(f"created: {created} ordered_date: {ordered_date} received_date: {recieved_date}")
        # print(f"department: {department}")
        print(f"employee: {employee}")
        print(f"supplier: {supplier} ")

        if supplier and employee and created:
            invoice = BarPurchase.objects.create(
                supplier_name=supplier,  # Assign the customer instance here
                created=created,
                status=status,
                sub_department=department,
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
                quantity = int(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                discount_price = float(request.POST.get(f"discount_amount_{i}", 0))

                product = get_object_or_404(BarProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},Discount amount: {discount_price}")

                if  product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    # Create and save the BarInvoiceDetail
                    detail = BarPurchaseItems.objects.create(
                        purchase_id=invoice,
                        product_name=product,
                        quantity=quantity,
                        selling_price=price,
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

        #return redirect("bar:purchases")

    context = {

        #"total_invoice": total_invoice,
        "form": form,
        "formset": formset,
    }

    return render(request, "bar/purchases/create_purchase.html", context)

@login_required
def edit_purchase(request, pk):
    # Fetch the existing invoice and its items
    invoice = get_object_or_404(BarPurchase, pk=pk)
    invoice_items = BarPurchaseItems.objects.filter(purchase_id=invoice)
    BarPurchaseItemsFormSet = modelformset_factory(BarPurchaseItems, form=BarPurchaseItemsForm, extra=0, can_delete=True)

    # Initialize the forms with existing invoice data
    form = BarPurchaseForm(instance=invoice)
    formset = BarPurchaseItemsFormSet(queryset=invoice_items)

    if request.method == "POST":
        # Extract the main form data from the POST request
        supplier_id = int(request.POST.get("supplier_name"))
        created = request.POST.get("created")
        status = request.POST.get("status")
        department = request.POST.get("sub_department")
        employee = request.POST.get("employee")
        
        # Fetch the supplier instance
        supplier = get_object_or_404(BarSupplier, pk=supplier_id)

        # Ensure all necessary fields are provided
        if supplier and employee and created:
            # Update the invoice object
            invoice.supplier_name = supplier
            invoice.created = created
            invoice.status = status
            invoice.sub_department = department
            invoice.employee = employee
            invoice.save()
            print("Invoice updated:", invoice)

            # Initialize the total
            total = 0

            # Process each row of invoice details
            row_count = int(request.POST.get("row_count", 0))  # Number of rows
            for i in range(1, row_count + 1):
                # detail_id = invoice_items[i].id if i < len(row_count) else None  # Handle case where there are fewer items than rows
                detail = invoice_items[i-1].id if invoice_items.exists() else None
                # Retrieve form data for the current row
                product_id = request.POST.get(f"raw_material{i}")
                quantity = int(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                discount_price = float(request.POST.get(f"discount_amount_{i}", 0))
                # detail_id = request.POST.get(f"detail_id_{i}")
                print(detail)
                # Fetch the product instance
                product = get_object_or_404(BarProduct, pk=product_id)
                price=product.selling_price

                if product and quantity and price:
                    
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")
                    
                    if i <= len(invoice_items):
                        detail = invoice_items[i-1]  # Update existing detail
                        detail.product_name = product
                        detail.quantity = quantity
                        detail.selling_price = price
                        detail.discount_amount = discount_price
                        
                        detail.save()
                        print(f"Updated detail for row {i}: {detail}")
                    else:
                        # If there are fewer details than rows, create new ones
                        detail = BarPurchaseItems.objects.create(
                            purchase_id=invoice,
                            product_name=product,
                            quantity=quantity,
                            selling_price=price,
                            discount_amount=discount_price,
                            
                        )
                        print(f"Created new detail for row {i}: {detail}")

                    # Update or create the BarPurchaseItems
                    # detail=BarPurchaseItems.objects.update_or_create(
                    #      # If detail exists, it updates. If not, it creates a new one.
                    #     purchase_id=invoice,
                    #     product_name=product,
                    #     defaults={
                    #         'quantity': quantity,
                    #         'selling_price': price,
                    #         'discount_amount': discount_price,
                    #     }
                    # )

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

    return render(request, "bar/purchases/create_purchase.html", context)


#--------------------------------------------------------------------#

# # BarInvoice view
# @login_required
# def purchase_invoice_payments_view(request):
#         invoice = BarInvoice.objects.all()
#         supplier = BarSupplier.objects.all()
#         purchase_invoice_payment = BarPurchasePayment.objects.all().order_by('-date')
#         #invoice_grand_total = list(invoices.aggregate(Sum('grand_total')).values())[0]

#         start_date = request.GET.get('start_date')
#         end_date = request.GET.get('end_date')

#         if start_date:
#             purchase_invoice_payment = purchase_invoice_payment.filter(created__range=[start_date, end_date])
#             #total_orders = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('amount')).values())[0]

#         else:
#             purchase_invoice_payment = purchase_invoice_payment
#             #total_orders = list(invoices.aggregate(Sum('amount')).values())[0]

#         template_name = 'bar/purchases/purchase_invoice_payments.html'
#         context = {
#                     'purchase_invoice_payment':purchase_invoice_payment,
#                     "invoice":invoice,
#                     "supplier":supplier ,

#                     }
#         return render(request, template_name, context)
    
# class add_purchase_payment_view(SuccessMessageMixin, CreateView):
#         model = BarPurchasePayment
#         template_name = 'bar/purchases/add_payment.html'
#         fields = '__all__'
#         #exclude = ('slug',)
#         success_url = reverse_lazy("bar:purchases")
#         success_message = 'Payment Transaction successful'

# # BarInvoice view
# class edit_purchase_payment_view(SuccessMessageMixin, UpdateView):
#         model = BarPurchasePayment
#         template_name = 'bar/purchases/edit_payment.html'
#         fields = '__all__'
#         #exclude = ('slug',)
#         success_url = reverse_lazy("bar:purchases")
#         success_message = 'Payment Transaction successfully Updated'







###################################SUPPLIER############################

# Create your views here.
@login_required
def suppliers_view(request):
    suppliers = BarSupplier.objects.all()

    template_name = 'bar/supplier/suppliers.html'
    context = {'suppliers':suppliers}
    return render(request, template_name, context)
#-------------------------------------------------------------------#
@login_required
def supplier_details(request, id):#
    supplier = get_object_or_404(BarSupplier, id=id)

    supplier_invoice = supplier.barpurchase_set.filter(status='Purchases')
    supplier_invoice_total = list(supplier_invoice.aggregate(Sum('purchase_total')).values())[0]

    purchase_returns = supplier.barpurchase_set.filter(status='Return Outwards')
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
    model = BarSupplier
    template_name = 'bar/supplier/forms/add_supplier.html'
    fields = '__all__'
    exclude = ('slug',)
    success_url = reverse_lazy('bar:supplier')
    success_message = 'supplier Account Successfully Created !!!'

#-------------------------------------------------------------------------#
class edit_supplier(SuccessMessageMixin, UpdateView):
    model = BarSupplier
    template_name = 'bar/supplier/forms/edit_supplier.html'
    fields = '__all__'
    exclude = ('slug',)
    success_url = reverse_lazy('bar:supplier')
    success_message = 'supplier Account Successfully Edited !!!'
#-------------------------------------------------------------------------#

########################PURCHASES##############
# Create your views here.
@login_required
def purchases_view(request):
    purchases = BarPurchase.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    #print(purchases)
    if start_date:
        purchases = purchases.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(purchases.filter(created__range=[start_date, end_date]).aggregate(Sum('purchase_total')).values())[0]

    else:
        purchases = purchases
        total_invoice_amount = list(purchases.aggregate(Sum('purchase_total')).values())[0]

    template_name = 'bar/purchases/purchase_invoices.html'
    context = {
                'purchases':purchases,
                'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)
 
    #--------------------------------------------------------#
#     # Detail view of invoices
# @login_required
# def purchase_detail(request, pk):
#     # Fetch the specific BarPurchase instance using its primary key (pk)
#     purchase = get_object_or_404(BarPurchase, id=pk)
    
#     # Get all associated BarPurchaseSummary objects related to this purchase
#     purchases_detail = BarPurchaseSummary.objects.filter(purchase_id=purchase)
    
#     # Fetch all payments related to this purchase
#     purchase_invoice_payments = BarPurchasePayment.objects.filter(invoice=purchase.id)
#     purchase_items = BarPurchaseItems.objects.filter(purchase_id=purchase.id)
#     # Calculate the total amount paid so far
#     total_payments = purchase_invoice_payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    
#     # Calculate the total number of payment installments
#     payment_installment_count = purchase_invoice_payments.count()
#     supplier = purchase.supplier_name
#     # Uncomment and modify the following lines if return items are needed
#     # return_items = purchase.returnsitems_set.all()
#     # total_returns = return_items.aggregate(Sum('total'))['total__sum'] or 0
#     print(purchase.department)
#     # Context to pass to the template
#     context = {
#         'purchase': purchase,
#         'purchases_detail': purchases_detail,
#         'purchase_invoice_payments': purchase_invoice_payments,
#         'total_payments': total_payments,
#         'payment_installment_count': payment_installment_count,
#         'supplier': supplier,
#         'purchase_items':purchase_items
#         # Uncomment if handling returns
#         # 'return_items': return_items,
#         # 'total_returns': total_returns,
#     }
    
#     # Render the template with the context
#     return render(request, "bar/purchases/purchases-invoice-template.html", context)
# #---------------------------------------------------------------------------------------#
# # BarInvoice view
# @login_required
# def create_purchase(request):

#     form = BarPurchaseForm()
#     formset = BarPurchaseItemsFormSet(queryset=BarPurchase.objects.none())
#     if request.method == "POST":
        
#         supplier_id=int(request.POST.get("supplier_name"))
#         created=request.POST.get("created")
#         ordered_date=timezone.make_aware(request.POST.get("ordered_date"))
#         recieved_date=timezone.make_aware(request.POST.get("recieved_date"))
#         department="Bar"
#         employee = request.POST.get("employee")
#         print(f"supplier_id (after conversion): {supplier_id}")
#         # print(f"department (after conversion): {department}")
#         supplier = get_object_or_404(BarSupplier, pk=supplier_id)
#         print(f"supplier_id: {supplier}")
#         print(f"created: {created} ordered_date: {ordered_date} received_date: {recieved_date}")
#         # print(f"department: {department}")
#         print(f"employee: {employee}")
#         print(f"supplier: {supplier} ")

#         if supplier and employee and created:
#             invoice = BarPurchase.objects.create(
#                 supplier_name=supplier,  # Assign the customer instance here
#                 created=created,
#                 ordered_date=ordered_date,
#                 recieved_date=recieved_date,
#                 # lead_time_days=lead_time_days,
#                 department=department,
#                 employee=employee
#             )
#             print("Invoice created:", invoice)
#             #-------------------- Invoice Created-------------------------#
            
#             #-------------------- InvoiceItems Starts Here-------------------------#
#             total = 0
#             print("total gotten")
            
#             # Process each row of invoice details
#             row_count = int(request.POST.get("row_count", 0))  # Number of rows
#             print("row gotten: ", row_count)
#             for i in range(1, row_count + 1):
#                 print("in for loop")
#                 product_id = request.POST.get(f"raw_material{i}")
#                 quantity = int(request.POST.get(f"quantity_{i}", 0))
#                 price = float(request.POST.get(f"price_{i}", 0))
#                 discount_price = float(request.POST.get(f"discount_amount_{i}", 0))

#                 product = get_object_or_404(BarProduct, pk=product_id)
#                 print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},Discount amount: {discount_price}")

#                 if  product and quantity and price:
#                     # Calculate the sum for each row
#                     row_total = float(price) * float(quantity)
#                     total += row_total  # Add to the total invoice amount
#                     print(f"Row {i} total: {row_total}, Cumulative total: {total}")

#                     # Create and save the BarInvoiceDetail
#                     detail = BarPurchaseItems.objects.create(
#                         purchase_id=invoice,
#                         raw_material=product,
#                         quantity=quantity,
#                         price=price,
#                         discount_amount=discount_price,
#                         ordered_date=ordered_date,
#                         recieved_date=recieved_date,
#                     )
#                     print(f"Saved detail for row {i}:", detail)

#             # Save the total invoice amount
#             invoice.purchase_total = total
#             invoice.save()
#             print("Invoice total saved:", invoice.purchase_total)

#             # Optionally, return a JSON response indicating success
#             return JsonResponse({"success": True, "invoice_id": invoice.id})

#         else:
#             print("Error: Missing required invoice data")
#             return JsonResponse({"success": False, "error": "Missing required invoice data"})

#         #return redirect("bakery:purchases")

#     context = {

#         #"total_invoice": total_invoice,
#         "form": form,
#         "formset": formset,
#     }

#     return render(request, "bar/purchases/create_purchase.html", context)
# #--------------------------------------------------------------------#

# # BarInvoice view
# @login_required
# def purchase_invoice_payments_view(request):
#         invoice = BarInvoice.objects.all()
#         supplier = BarSupplier.objects.all()
#         purchase_invoice_payment = BarPurchasePayment.objects.all().order_by('-date')
#         #invoice_grand_total = list(invoices.aggregate(Sum('grand_total')).values())[0]

#         start_date = request.GET.get('start_date')
#         end_date = request.GET.get('end_date')

#         if start_date:
#             purchase_invoice_payment = purchase_invoice_payment.filter(created__range=[start_date, end_date])
#             #total_orders = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('amount')).values())[0]

#         else:
#             purchase_invoice_payment = purchase_invoice_payment
#             #total_orders = list(invoices.aggregate(Sum('amount')).values())[0]

#         template_name = 'bar/purchases/purchase_invoice_payments.html'
#         context = {
#                     'purchase_invoice_payment':purchase_invoice_payment,
#                     "invoice":invoice,
#                     "supplier":supplier ,

#                     }
#         return render(request, template_name, context)
    
# class add_purchase_payment_view(SuccessMessageMixin, CreateView):
#         model = BarPurchasePayment
#         template_name = 'bar/purchases/add_payment.html'
#         fields = '__all__'
#         #exclude = ('slug',)
#         success_url = reverse_lazy("bakery:purchases")
#         success_message = 'Payment Transaction successful'

# # BarInvoice view
# class edit_purchase_payment_view(SuccessMessageMixin, UpdateView):
#         model = BarPurchasePayment
#         template_name = 'bar/purchases/edit_payment.html'
#         fields = '__all__'
#         #exclude = ('slug',)
#         success_url = reverse_lazy("bakery:purchases")
#         success_message = 'Payment Transaction successfully Updated'








#--------------------------------------------------------#
# Detail view of inventories
 
@login_required
def inventory_view(request):
    inventory = BarInventory.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        inventory = inventory.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(inventory.filter(created__range=[start_date, end_date]).aggregate(Sum('total_price')).values())[0]

    else:
        inventory = inventory
        total_invoice_amount = list(inventory.aggregate(Sum('total_price')).values())[0]
    print(total_invoice_amount)
    template_name = 'bar/inventory/inventory.html'
    context = {
                'inventory':inventory,
                'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)

class BarInventoryDetailView(DetailView):
    model = BarInventory
    template_name = 'bar/inventory/inventory-detail-template.html'  # Customize this to your actual template path
    context_object_name = 'inventory'  # The context variable name for the object in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch related inventory items and add them to the context
        context['inventory_items'] = BarInventoryItems.objects.filter(inventory_id=self.object)
        return context


#--------------------------------------------------------#
def create_inventory(request):
    form = BarInventoryForm()
    formset = BarInventoryItemsFormSet(queryset=BarInventoryItems.objects.none())
    if request.method == "POST":
        # Extract the main form data from the POST request
        employee = request.POST.get("employee")
        created = request.POST.get("created")
        description = request.POST.get("description")
        

        # Print the extracted values
        print(f"employee: {employee}")
        print(f"created: {created}")
        print(f"description: {description}")

        # Fetch the customer instance
        #customer = get_object_or_404(BarCustomer, pk=customer_id)

        # Print the customer instance to verify it's fetched correctly
        

        # Create the invoice object
        if employee and created:
            invoice = BarInventory.objects.create(
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
                
                product = get_object_or_404(BarProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},status: {status}")

                if  product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    # Create and save the BarInvoiceDetail
                    detail = BarInventoryItems.objects.create(
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
    return render(request, "bar/inventory/create_inventory.html", context)

@login_required
def edit_inventory(request, pk):
    # Fetch the existing inventory and its items
    invoice = get_object_or_404(BarInventory, pk=pk)
    invoice_items = BarInventoryItems.objects.filter(inventory_id=invoice)
    BarInventoryItemsFormSet = modelformset_factory(BarInventoryItems, form=BarInventoryItemsForm, extra=0, can_delete=True)

    # Initialize the forms with existing inventory data
    form = BarInventoryForm(instance=invoice)
    formset = BarInventoryItemsFormSet(queryset=invoice_items)

    if request.method == "POST":
        # Extract the main form data from the POST request
        employee = request.POST.get("employee")
        created = request.POST.get("created")
        description = request.POST.get("description")
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

                product = get_object_or_404(BarProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price}, Status: {status}")

                if product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    if i <= len(invoice_items):
                        # Update existing detail
                        detail = invoice_items[i - 1]
                        detail.product_name = product
                        detail.quantity = quantity
                        detail.selling_price = price
                        detail.status = status
                        detail.save()
                        print(f"Updated detail for row {i}: {detail}")
                    else:
                        # Create new detail if there are more rows than existing items
                        detail = BarInventoryItems.objects.create(
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

    return render(request, "bar/inventory/create_inventory.html", context)


####FOR AJAX BarInvoice Create
# def get_customer_name(request):
#     if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         product_id = request.GET.get('product_id')
#         print(product_id)
#         try:
#             #product = BarCustomer.objects.get(id=product_id)
#             product = get_object_or_404(BarInvoice, pk=product_id)
#             print(product)
#             customer_name = product.customer.customer_name
#             customer_id = product.customer_id
#             return JsonResponse({'price': customer_name, 'id':customer_id})
#         except BarCustomer.DoesNotExist:
#             return JsonResponse({'error': 'Product not found'}, status=404)
#     return JsonResponse({'error': 'Invalid request'}, status=400)


def get_product_price(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.GET.get('product_id')
        try:
            product = BarProduct.objects.get(id=product_id)
            return JsonResponse({'price': product.price})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

# def get_raw_price(request):
#     if request.method == 'GET':
#         rm_id = request.GET.get('rm_id')
#         try:
#             product = BarPurchaseItems.objects.filter(raw_material=rm_id).order_by('created').last()
#             return JsonResponse({'price': product.price})
#         except Product.DoesNotExist:
#             return JsonResponse({'error': 'Product not found'}, status=404)
#     return JsonResponse({'error': 'Invalid request'}, status=400)


# def add_more_row(request):
#     formset = BarInvoiceDetailFormSet(prefix='form')
#     empty_form = formset.empty_form
#     rendered_row = render_to_string('bar/invoice/new_row.html', {'form': empty_form})
#     return JsonResponse({'row_html': rendered_row})


def add_more_row_purchase(request):
    formset = BarPurchaseItemsFormSet(prefix='form')
    empty_form = formset.empty_form
    rendered_row = render_to_string('bar/purchases/new_row.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})

def add_more_row_inventory(request):
    formset = BarInventoryItemsFormSet(prefix='form')
    empty_form = formset.empty_form
    rendered_row = render_to_string('bar/inventory/new_row.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})

# def add_more_row_output(request):
#     formset2 = BarProductionOutputFormset(prefix='form')
#     empty_form = formset2.empty_form
#     rendered_row = render_to_string('bar/production/new_row_output.html', {'form': empty_form})
#     return JsonResponse({'row_html': rendered_row})
