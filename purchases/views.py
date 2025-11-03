from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import *
from django.db.models import Sum
from django.db.models import Q

from .models import *
from customer.models import *
from product.models import *
# Create your views here.
from django.contrib.auth.decorators import login_required
from .forms import InvoicesDetailFormSet, InvoicesForm
from .forms import *

from django.core.paginator import Paginator
# Invoice view

# Create your views here.
@login_required
def purchases_view(request):
    purchases = Invoices.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        purchases = purchases.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(purchases.filter(created__range=[start_date, end_date]).aggregate(Sum('invoice_total')).values())[0]

    else:
        purchases = purchases
        total_invoice_amount = list(purchases.aggregate(Sum('invoice_total')).values())[0]

    template_name = 'purchases/purchase_invoices.html'
    context = {
                'purchases':purchases,
                'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)
 
    #--------------------------------------------------------#
    # Detail view of invoices
@login_required
def purchase_detail(request, pk):

    invoice = Invoices.objects.get(id=pk)
    purchases_detail = InvoicesDetail.objects.filter(invoice=invoice)

    #items = invoice.invoicedetail_set.all()
    #items_total = list(items.aggregate(Sum('total')).values())[0]

    purchase_invoice_payments = invoice.purchaseinvoicespayment_set.all()
    total_payments = list(purchase_invoice_payments.aggregate(Sum('amount_paid')).values())[0]
    #payment_installment_count = invoice_payments.count()

    #return_items = invoice.returnsitems_set.all()
    #total_returns = list(return_items.aggregate(Sum('total')).values())[0]



    context = {
        'invoice': invoice,
        "purchases_detail": purchases_detail,
        #'items_total':items_total,
        'purchase_invoice_payments':purchase_invoice_payments,
        'total_payments':total_payments,
        #'payment_installment_count':payment_installment_count,

        #"return_items":return_items,
        #'total_returns':total_returns,

    }

    return render(request, "purchases/purchases-invoice-template.html", context)
#---------------------------------------------------------------------------------------#
# Invoice view
@login_required
def create_purchase(request):

    form = InvoicesForm()
    formset = InvoicesDetailFormSet()
    if request.method == "POST":
        form = InvoicesForm(request.POST)
        formset = InvoicesDetailFormSet(request.POST)
        if form.is_valid():
            invoice = Invoices.objects.create(
                supplier=form.cleaned_data.get("supplier"),
                created=form.cleaned_data.get("created"),
                sub_department=form.cleaned_data.get("sub_department"),
                employee = form.cleaned_data.get("employee"),
            )
        if formset.is_valid():
            total = 0
            for form in formset:
                product = form.cleaned_data.get("product")
                quantity = form.cleaned_data.get("quantity")
                price = form.cleaned_data.get("price")
                if product and quantity and price:
                    # Sum each row
                    sum = float(price) * float(quantity)
                    # Sum of total invoice
                    total += sum
                    InvoicesDetail(
                        invoice=invoice,
                        product=product,
                        quantity=quantity,
                        price=price
                    ).save()
            # Pointing the customer
            # Save the invoice
            #invoice.invoice_total = total
            invoice.save()
            return redirect("purchases:purchases")

    context = {

        #"total_invoice": total_invoice,
        "form": form,
        "formset": formset,
    }

    return render(request, "purchases/create_purchase.html", context)
#--------------------------------------------------------------------#

# Invoice view
@login_required
def purchase_invoice_payments_view(request):
        invoice = Invoices.objects.all()
        supplier = Supplier.objects.all()
        purchase_invoice_payment = PurchaseInvoicesPayment.objects.all().order_by('-date')
        #invoice_grand_total = list(invoices.aggregate(Sum('grand_total')).values())[0]

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date:
            purchase_invoice_payment = purchase_invoice_payment.filter(created__range=[start_date, end_date])
            #total_orders = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('amount')).values())[0]

        else:
            purchase_invoice_payment = purchase_invoice_payment
            #total_orders = list(invoices.aggregate(Sum('amount')).values())[0]

        template_name = 'purchases/purchase_invoice_payments.html'
        context = {
                    'purchase_invoice_payment':purchase_invoice_payment,
                    "invoice":invoice,
                    "supplier":supplier ,

                    }
        return render(request, template_name, context)
class add_purchase_payment_view(SuccessMessageMixin, CreateView):
        model = PurchaseInvoicesPayment
        template_name = 'purchases/add_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("purchases:purchases")
        success_message = 'Payment Transaction successful'

# Invoice view
class edit_purchase_payment_view(SuccessMessageMixin, UpdateView):
        model = PurchaseInvoicesPayment
        template_name = 'purchases/edit_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("purchases:purchases")
        success_message = 'Payment Transaction successfully Updated'

from django.http import JsonResponse
from .models import Product  # Replace with your actual product model

def get_product_price(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.GET.get('product_id')
        try:
            product = Supplier.objects.get(id=product_id)
            return JsonResponse({'price': product.price})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_customer_name(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.GET.get('product_id')
        try:
            product = Supplier.objects.get(id=product_id)
            customer_name = product.customer.customer_name
            customer_id = product.customer_id
            return JsonResponse({'price': customer_name, 'id':customer_id})
        except Supplier.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


# views.py
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import InvoicesDetailFormSet  # Adjust the import based on your formset name

def add_more_row(request):
    formset = InvoicesDetailFormSet(prefix='form')
    empty_form = formset.empty_form
    rendered_row = render_to_string('purchases/new_row.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})
