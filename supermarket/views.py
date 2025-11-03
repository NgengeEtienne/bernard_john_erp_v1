from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
#from .forms import *
from django.db.models import Sum
from django.db.models import Q
from configuration.models import Department
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
def view(request):
    # Your homepage logic (e.g., display featured content)
    return render(request, 'supermarket/index.html')

# Create your views here.
def invoice_view(request):
    invoices = SupermarketInvoice.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        invoices = invoices.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('invoice_total')).values())[0]

    else:
        invoices = invoices
        total_invoice_amount = list(invoices.aggregate(Sum('invoice_total')).values())[0]

    template_name = 'supermarket/invoice/invoices.html'
    context = {
                'invoices':invoices,
                'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)

#############   #############   #############   #############   #############
#------------------------- Customer Views ------------------------------#
#############   #############   #############   #############   #############
class SupermarketCustomerListView(ListView):
    model = SupermarketCustomer
    template_name = 'supermarket/bakery_customer/customers.html'  # Specify your template name
    context_object_name = 'customers'  # The name to use in the template
    paginate_by = 1000  # Number of customers per page

    def get_queryset(self):
        return SupermarketCustomer.objects.all().order_by('customer_name')  # Order by customer name

    
class SupermarketCustomerDetailView(DetailView):
    model = SupermarketCustomer
    template_name = 'supermarket/bakery_customer/customer_account.html'  # Specify your template name
    context_object_name = 'customer'  # The name to use in the template
    slug_field = 'slug'  # Use slug field for URL lookup
    slug_url_kwarg = 'slug'  # The name of the slug URL parameter

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(SupermarketCustomer, slug=slug)
    
class SupermarketCustomerCreateView(View):
    def get(self, request):
        form = SupermarketCustomerForm()
        return render(request, 'supermarket/bakery_customer/add_customer_form.html', {'form': form})

    def post(self, request):
        form = SupermarketCustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            print(customer)
            return redirect('supermarket:customer-list')  # Redirect to customer list after successful creation
        return render(request, 'supermarket/bakery_customer/add_customer_form.html', {'form': form})  
    
class SupermarketCustomerEditView(UpdateView):
    model = SupermarketCustomer
    form_class = SupermarketCustomerForm
    template_name = 'supermarket/bakery_customer/edit_customer_form.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(SupermarketCustomer, slug=slug)

    def form_valid(self, form):
        form.save()
        return redirect('supermarket:customers')  # Redirect to the customer list after saving    
    
#############   #############   #############   #############   #############
#------------------------- Product Views ------------------------------#
#############   #############   #############   #############   ############# 
class SupermarketProductCategoryListView(ListView):
    model = SupermarketProductCategory
    template_name = 'supermarket/bakery_product/categories.html'  # Specify your template name
    context_object_name = 'categories'  # The name to use in the template
    paginate_by = 10  # Number of categories per page

    def get_queryset(self):
        return SupermarketProductCategory.objects.all().order_by('category_name')  # Order by category name


class SupermarketProductCategoryDetailView(DetailView):
    model = SupermarketProductCategory
    template_name = 'supermarket/bakery_product/category_detail.html'  # Specify your template name
    context_object_name = 'category'  # The name to use in the template
    slug_field = 'slug'  # Use slug field for URL lookup
    slug_url_kwarg = 'slug'  # The name of the slug URL parameter


class SupermarketProductCategoryCreateView(CreateView):
    model = SupermarketProductCategory
    form_class = SupermarketProductCategoryForm  # Ensure you have a form for this model
    template_name = 'supermarket/bakery_product/add_category_form.html'  # Specify your template name

    def form_valid(self, form):
        form.save()
        return redirect('supermarket:category-list')  # Redirect to category list after successful creation
    


class SupermarketProductCategoryEditView(UpdateView):
    model = SupermarketProductCategory
    form_class = SupermarketProductCategoryForm
    template_name = 'supermarket/bakery_product/edit_category_form.html'  # Specify your template name

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(SupermarketProductCategory, pk=pk)

    def form_valid(self, form):
        form.save()
        return redirect('supermarket:category-list')  # Redirect to the category list after saving



    
#--------------------------------------------------------#
# Detail view of invoices
def invoice_detail(request, pk):

    invoice = SupermarketInvoice.objects.get(id=pk)
    invoice_detail = SupermarketInvoiceDetail.objects.filter(invoice=invoice)

    items = invoice.supermarketinvoicedetail_set.all()
    items_total = list(items.aggregate(Sum('total')).values())[0]

    invoice_payments = invoice.supermarketinvoicepayment_set.all()
    total_payments = list(invoice_payments.aggregate(Sum('amount_paid')).values())[0]
    payment_installment_count = invoice_payments.count()

    return_items = invoice.supermarketreturnsitems_set.all()
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

    return render(request, "supermarket/invoice/invoice-template.html", context)

from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
def create_invoice(request):
    form = SupermarketInvoiceForm()
    formset = SupermarketInvoiceDetailFormSet()
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
        customer = get_object_or_404(SupermarketCustomer, pk=customer_id)

        # Print the customer instance to verify it's fetched correctly
        print(f"customer: {customer}")

        # Create the invoice object
        if sales_person and customer and created and sales_session:
            invoice = SupermarketInvoice.objects.create(
                customer=customer,  # Assign the customer instance here
                created=created,
                sales_session=sales_session,
                sales_person=sales_person,
                status=status,
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
                quantity = int(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                discount_price = float(request.POST.get(f"discount_price_{i}", 0))

                product = get_object_or_404(SupermarketProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},Discount Price: {discount_price}")

                if  product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    # Create and save the SupermarketInvoiceDetail
                    detail = SupermarketInvoiceDetail.objects.create(
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
    form = SupermarketInvoiceForm()
    context = {
        "form": form,
        'formset': formset,
        }
    return render(request, "supermarket/invoice/create_invoice.html", context)


#--------------------------------------------------------------------#
# Edit Invoice view
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .models import SupermarketInvoice, SupermarketInvoiceDetail
from .forms import SupermarketInvoiceForm, SupermarketInvoiceDetailForm

def edit_invoice(request, pk):
    print("edit_invoice() called with pk:", pk)

    invoice = get_object_or_404(SupermarketInvoice, pk=pk)
    invoice_items = SupermarketInvoiceDetail.objects.filter(invoice=invoice)

    # Create a model formset for SupermarketInvoiceDetail
    SupermarketInvoiceDetailFormSet = modelformset_factory(SupermarketInvoiceDetail, form=SupermarketInvoiceDetailForm, extra=0, can_delete=True)
    form = SupermarketInvoiceForm(instance=invoice)
    formset = SupermarketInvoiceDetailFormSet(queryset=invoice_items)
    if request.method == "POST":
        # Extract the main form data from the POST request
        customer_id = request.POST.get("customer")
        created = request.POST.get("created")
        sales_session = request.POST.get("sales_session")
        sales_person = request.POST.get("sales_person")
        status = request.POST.get("status")

        # Print the extracted values
        # print(f"customer_id: {customer_id}")
        # print(f"created: {created}")
        # print(f"sales_session: {sales_session}")
        # print(f"sales_person: {sales_person}")
        # print(f"status: {status}")
        # Fetch the customer instance
        customer = get_object_or_404(SupermarketCustomer, pk=customer_id)

        # Print the customer instance to verify it's fetched correctly
        print(f"customer: {customer}")

        # Update the invoice object
        if sales_person and customer and created and sales_session:
            invoice.customer = customer
            invoice.created = created
            invoice.sales_session = sales_session
            invoice.sales_person = sales_person
            invoice.status = status
            invoice.save()
            print("Invoice updated:", invoice)

            # Initialize total
            total = 0
            print("init total : ", total)
            # Process each row of invoice details
            row_count = int(request.POST.get("row_count", 0))  # Number of rows
            # print("row gotten: ", row_count)

  # Ensure you have the row count

            for i in range(1, row_count + 1):
                print("Processing row:", i)
                print("in for total : ", total)
                # Retrieve form data for the current row
                product_id = request.POST.get(f"product_{i}")
                quantity = int(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                discount_price = float(request.POST.get(f"discount_price_{i}", 0))
                id = float(request.POST.get(f"id_{i}", 0))

                if not product_id:
                    print(f"Skipping row {i} due to missing product_id")
                    continue

                product = get_object_or_404(SupermarketProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price}, Discount Price: {discount_price}")

                if quantity and price:
                    discount_value = quantity * discount_price
                    # Calculate the sum for each row
                    row_total = (float(price) * float(quantity)) - discount_value
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    
                    row_total_with_discount = row_total

                    # Update or create the SupermarketInvoiceDetail
                    detail, created = SupermarketInvoiceDetail.objects.update_or_create(
                        id=id,
                        invoice=invoice,
                        product=product,
                        defaults={
                            'quantity': quantity,
                            'price': price,
                            'discount_price': discount_price,
                            'discount_value': discount_value,
                            'net_amount': row_total_with_discount,
                        }
                    )
                

                    print(f"Saved detail for row {i}: {detail}")
                    # print(f"Created new detail: {created}")

           
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
    return render(request, 'supermarket/invoice/edit_invoice.html', context)


# Invoice view
def InvoicePayment_view(request):
        invoice = SupermarketInvoice.objects.all()
        customer = Customer.objects.all()
        invoice_payment = SupermarketInvoicePayment.objects.all().order_by('-date')
        #invoice_grand_total = list(invoices.aggregate(Sum('grand_total')).values())[0]

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date:
            invoice_payment = invoice_payment.filter(created__range=[start_date, end_date])
        else:
            invoice_payment = SupermarketInvoicePayment.objects.all().order_by('-date')
            #total_orders = list(invoices.aggregate(Sum('amount')).values())[0]

        template_name = 'supermarket/invoice/invoice_payments.html'
        context = {
                    'invoice_payment':invoice_payment,
                    "invoice":invoice,
                    "customer":customer ,

                    }
        return render(request, template_name, context)

class add_payment_view(SuccessMessageMixin, CreateView):
        model = SupermarketInvoicePayment
        template_name = 'supermarket/invoice/add_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("supermarket:invoice-payments")
        success_message = 'Payment Transaction successful'

# Invoice view
class edit_payment_view(SuccessMessageMixin, UpdateView):
        model = SupermarketInvoicePayment
        template_name = 'supermarket/invoice/edit_payment.html'
        fields = '__all__'
        #exclude = ('slug',)

        def get_object(self):
            pk = self.kwargs.get('pk')
            return SupermarketInvoicePayment.objects.get(pk=pk)

        def get_success_url(self):
            print("Edit Payment View: get success url")
            return reverse_lazy("supermarket:invoice-payments")

        def get_success_message(self, cleaned_data):
            print("Edit Payment View: get success message")
            return 'Payment Transaction for Invoice {} successfully Updated'.format(self.object.invoice)

        def get_context_data(self, **kwargs):
            context = super(edit_payment_view, self).get_context_data(**kwargs)
            print("Edit Payment View: get context data")
            print(context)
            context['invoice_payment'] = self.object
            return context

class add_returns_view(SuccessMessageMixin, CreateView):
        model = SupermarketReturnsItems
        template_name = 'supermarket/invoice/add_returns.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy('supermarket:invoice-payments')
        success_message = 'Payment Transaction successful'



########################PURCHASES##############
# Create your views here.
@login_required
def purchases_view(request):
    purchases = SupermarketPurchase.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    print(purchases)
    if start_date:
        purchases = purchases.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(purchases.filter(created__range=[start_date, end_date]).aggregate(Sum('purchase_total')).values())[0]

    else:
        purchases = purchases
        total_invoice_amount = list(purchases.aggregate(Sum('purchase_total')).values())[0]

    template_name = 'supermarket/purchases/purchase_invoices.html'
    context = {
                'purchases':purchases,
                'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)
 
    #--------------------------------------------------------#
    # Detail view of invoices
@login_required
def purchase_detail(request, pk):

    purchase = get_object_or_404(SupermarketPurchase, id=pk)
    
    # Get all associated BakeryPurchaseSummary objects related to this purchase
    purchases_detail = SupermarketPurchaseSummary.objects.filter(purchase_id=purchase)
    
    # Fetch all payments related to this purchase
    purchase_invoice_payments = SupermarketPurchasePayment.objects.filter(invoice=purchase.id)
    purchase_items = SupermarketPurchaseItems.objects.filter(purchase_id=purchase.id)
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
    return render(request, "supermarket/purchases/purchase-invoice-template.html", context)
#---------------------------------------------------------------------------------------#
# SupermarketInvoice view
@login_required
def create_purchase(request):

    form = SupermarketPurchaseForm()
    formset = SupermarketPurchaseItemsFormSet(queryset=SupermarketPurchase.objects.none())
    if request.method == "POST":
        
        supplier_id=int(request.POST.get("supplier_name"))
        created=request.POST.get("created")
        ordered_date=request.POST.get("ordered_date")
        recieved_date=request.POST.get("recieved_date")
        department = Department.objects.filter(department_name="Supermarket").first()
        employee = request.POST.get("employee")
        print(f"supplier_id (after conversion): {supplier_id}")
        print(f"sub_department (after conversion): {department}")
        supplier = get_object_or_404(SupermarketSupplier, pk=supplier_id)
        print(f"supplier_id: {supplier}")
        print(f"created: {created} ordered_date: {ordered_date} received_date: {recieved_date}")
        print(f"department: {department}")
        print(f"employee: {employee}")
        print(f"supplier: {supplier} ")

        if supplier and employee and created:
            invoice = SupermarketPurchase.objects.create(
                supplier_name=supplier,  # Assign the customer instance here
                created=created,
                ordered_date=ordered_date,
                recieved_date=recieved_date,
                # department=department,
                employee=employee
            )
            print("Invoice created:", invoice)
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

                product = get_object_or_404(SupermarketProduct, pk=product_id)
                print(f"Processing row {i} - Product: {product}, Quantity: {quantity}, Price: {price},Discount amount: {discount_price}")

                if  product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")

                    # Create and save the SupermarketInvoiceDetail
                    detail = SupermarketPurchaseItems.objects.create(
                        purchase_id=invoice,
                        product=product,
                        quantity=quantity,
                        unit_cost_price=price,
                        discount_price=discount_price,
                        ordered_date=ordered_date,
                        recieved_date=recieved_date,
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

        #return redirect("supermarket:purchases")

    context = {

        #"total_invoice": total_invoice,
        "form": form,
        "formset": formset,
    }

    return render(request, "supermarket/purchases/create_purchase.html", context)
#--------------------------------------------------------------------#@login_required
def edit_purchase(request, pk):
    # Fetch the existing invoice and its items
    invoice = get_object_or_404(SupermarketPurchase, pk=pk)
    invoice_items = SupermarketPurchaseItems.objects.filter(purchase_id=invoice)
    BarPurchaseItemsFormSet = modelformset_factory(SupermarketPurchaseItems, form=SupermarketPurchaseItemsForm, extra=0, can_delete=True)

    # Initialize the forms with existing invoice data
    form = SupermarketPurchaseForm(instance=invoice)
    formset = BarPurchaseItemsFormSet(queryset=invoice_items)

    if request.method == "POST":
        # Extract the main form data from the POST request
        supplier_id = int(request.POST.get("supplier_name"))
        created = request.POST.get("created")
        ordered_date = request.POST.get("ordered_date")
        recieved_date = request.POST.get("recieved_date")
        department = Department.objects.filter(department_name="Supermarket").first()
        employee = request.POST.get("employee")
        print(f"department: {department}")
        # Fetch the supplier instance
        supplier = get_object_or_404(SupermarketSupplier, pk=supplier_id)

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
            for i in range(1, row_count + 1):
                detail = invoice_items[i-1] if i-1 < len(invoice_items) else (invoice_items.first() if invoice_items.exists() else None)

                
                # Retrieve form data for the current row
                product_id = request.POST.get(f"raw_material{i}")
                quantity = int(request.POST.get(f"quantity_{i}", 0))
                price = float(request.POST.get(f"price_{i}", 0))
                discount_price = float(request.POST.get(f"discount_amount_{i}", 0))

                # Fetch the product instance
                product = get_object_or_404(SupermarketProduct, pk=product_id)
                price = product.selling_price

                if product and quantity and price:
                    # Calculate the sum for each row
                    row_total = float(price) * float(quantity)
                    total += row_total  # Add to the total invoice amount
                    print(f"Row {i} total: {row_total}, Cumulative total: {total}")
                    
                    if i <= len(invoice_items):
                        # Update existing detail
                        detail = invoice_items[i-1]
                        detail.product = product
                        detail.quantity = quantity
                        detail.unit_cost_price = price
                        detail.discount_price = discount_price
                        detail.ordered_date = ordered_date
                        detail.recieved_date = recieved_date
                        detail.save()
                        print(f"Updated detail for row {i}: {detail}")
                    else:
                        # If there are fewer details than rows, create new ones
                        detail = SupermarketPurchaseItems.objects.create(
                            purchase_id=invoice,
                            product=product,
                            quantity=quantity,
                            unit_cost_price=price,
                            discount_price=discount_price,
                            ordered_date=ordered_date,
                            recieved_date=recieved_date
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

    return render(request, "supermarket/purchases/create_purchase.html", context)

# SupermarketInvoice view
@login_required
def purchase_invoice_payments_view(request):
        invoice = SupermarketInvoice.objects.all()
        supplier = SupermarketSupplier.objects.all()
        purchase_invoice_payment = SupermarketPurchasePayment.objects.all().order_by('-date')
        #invoice_grand_total = list(invoices.aggregate(Sum('grand_total')).values())[0]

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date:
            purchase_invoice_payment = purchase_invoice_payment.filter(created__range=[start_date, end_date])
            #total_orders = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('amount')).values())[0]

        else:
            purchase_invoice_payment = purchase_invoice_payment
            #total_orders = list(invoices.aggregate(Sum('amount')).values())[0]

        template_name = 'supermarket/purchases/purchase_invoice_payments.html'
        context = {
                    'purchase_invoice_payment':purchase_invoice_payment,
                    "invoice":invoice,
                    "supplier":supplier ,

                    }
        return render(request, template_name, context)
class add_purchase_payment_view(SuccessMessageMixin, CreateView):
        model = SupermarketPurchasePayment
        template_name = 'supermarket/purchases/add_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("supermarket:purchases")
        success_message = 'Payment Transaction successful'

# SupermarketInvoice view
class edit_purchase_payment_view(SuccessMessageMixin, UpdateView):
        model = SupermarketPurchasePayment
        template_name = 'supermarket/purchases/edit_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("supermarket:purchases")
        success_message = 'Payment Transaction successfully Updated'







###################################SUPPLIER############################

# Create your views here.
@login_required
def suppliers_view(request):
    suppliers = SupermarketSupplier.objects.all()

    template_name = 'supermarket/supplier/suppliers.html'
    context = {'suppliers':suppliers}
    return render(request, template_name, context)
#-------------------------------------------------------------------#
@login_required
def supplier_details(request, id):#
    supplier = get_object_or_404(SupermarketSupplier, id=id)



    supplier_invoice = supplier.supermarketpurchase_set.all()
    supplier_invoice_total = list(supplier_invoice.aggregate(Sum('purchase_total')).values())[0]
    #opening_balance = customers.customeropeningbalance_set.all()
    #returns = customers.returnsitems_set.all()
    #returns_total = list(returns.aggregate(Sum('total')).values())[0]


    # purchase_payments =supplier.purchaseinvoicespayment_set.all()
    # total_purchase_payment= list(purchase_payments.aggregate(Sum('amount_paid')).values())[0]

    template_name = 'supermarket/supplier/supplier_account.html'
    context = {'supplier':supplier,
                #'opening_balance':opening_balance,
                'supplier_invoice':supplier_invoice,
                'supplier_invoice_total':supplier_invoice_total,

                # 'purchase_payments':purchase_payments,
                # 'total_purchase_payment':total_purchase_payment,
                }
 
    return render(request, template_name, context)
#-------------------------------------------------------------------------#
class add_supplier(SuccessMessageMixin, CreateView):
    model = SupermarketSupplier
    template_name = 'supermarket/supplier/forms/add_supplier.html'
    fields = '__all__'
    exclude = ('slug',)
    success_url = reverse_lazy('supermarket:supplier')
    success_message = 'supplier Account Successfully Created !!!'

#-------------------------------------------------------------------------#
class edit_supplier(SuccessMessageMixin, UpdateView):
    model = SupermarketSupplier
    template_name = 'supermarket/supplier/forms/edit_supplier.html'
    fields = '__all__'
    exclude = ('slug',)
    success_url = reverse_lazy('supermarket:supplier')
    success_message = 'supplier Account Successfully Edited !!!'
#-------------------------------------------------------------------------#



####FOR AJAX
def get_customer_name(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.GET.get('product_id')
        print(product_id)
        try:
            #product = SupermarketCustomer.objects.get(id=product_id)
            product = get_object_or_404(SupermarketInvoice, pk=product_id)
            print(product)
            customer_name = product.customer.customer_name
            customer_id = product.customer_id
            return JsonResponse({'price': customer_name, 'id':customer_id})
        except SupermarketCustomer.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_product_price(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.GET.get('product_id')
        try:
            product = SupermarketProduct.objects.get(id=product_id)
            return JsonResponse({'price': product.selling_price })
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def add_more_row(request):
    formset = SupermarketInvoiceDetailFormSet(prefix='form')
    empty_form = formset.empty_form
    rendered_row = render_to_string('supermarket/invoice/new_row.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})


def add_more_row_purchase(request):
    formset = SupermarketPurchaseItemsFormSet(prefix='form')
    empty_form = formset.empty_form
    rendered_row = render_to_string('supermarket/purchases/new_row.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})
