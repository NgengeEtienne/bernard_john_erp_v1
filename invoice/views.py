from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import *
from django.db.models import Sum
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import *
from customer.models import *
from product.models import *
# Create your views here.

from .forms import InvoiceDetailFormSet, InvoiceForm
from .forms import *
# from .forms import PurchaseItems

from django.core.paginator import Paginator
# Invoice view
@login_required
def homepage(request):
    # Your homepage logic (e.g., display featured content)
    return render(request, 'root.html')


# Create your views here.
@login_required
def invoice_view(request):
    invoices = Invoice.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        invoices = invoices.filter(created__range=[start_date, end_date])
        total_invoice_amount = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('invoice_total')).values())[0]

    else:
        invoices = invoices
        total_invoice_amount = list(invoices.aggregate(Sum('invoice_total')).values())[0]

    template_name = 'invoice/invoices.html'

   
    context = {
                'invoices':invoices,
                'total_invoice_amount':total_invoice_amount,
                }
    return render(request, template_name, context)

#--------------------------------------------------------#
#Get customer in ajax
@login_required
def search_customers(request):
    query = request.GET.get('q', '')
    customers = Invoice.objects.filter(name__icontains=query).values('id','name')
    return JsonResponse({'customers': list(customers)})
#--------------------------------------------------------#
# Detail view of invoices
@login_required
def invoice_detail(request, pk):

    invoice = Invoice.objects.get(id=pk)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)

    items = invoice.invoicedetail_set.all() 
    items_total = list(items.aggregate(Sum('total')).values())[0]

    invoice_payments = invoice.invoicepayment_set.all()
    total_payments = list(invoice_payments.aggregate(Sum('amount_paid')).values())[0]
    payment_installment_count = invoice_payments.count()

    return_items = invoice.returnsitems_set.all()
    total_returns = list(return_items.aggregate(Sum('total')).values())[0]



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
 
    return render(request, "invoice/invoice-template.html", context)


@login_required
def create_invoice(request):
    form = InvoiceForm()
    formset = InvoiceDetailFormSet()

    if request.method == "POST":
        form = InvoiceForm(request.POST)
        formset = InvoiceDetailFormSet(request.POST)
        invoice_total = request.POST.get('invoice_total')

        if form.is_valid():
            invoice = Invoice.objects.create(
                customer=form.cleaned_data.get("customer"),
                created=form.cleaned_data.get("created"),
                sales_session=form.cleaned_data.get("sales_session"),
                invoice_total=invoice_total,
            )
            print(f"Invoice created: {invoice}")

        if formset.is_valid():
            print("Formset is valid")
            total = 0
            for detail_form in formset:
                sales_person = detail_form.cleaned_data.get("sales_person")
                product = detail_form.cleaned_data.get("product")
                quantity = detail_form.cleaned_data.get("quantity")
                price = detail_form.cleaned_data.get("price")

                if sales_person and product and quantity and price:
                    sum = float(price) * float(quantity)
                    total += sum
                    invoice_detail = InvoiceDetail.objects.create(
                        invoice=invoice,
                        sales_person=sales_person,
                        product=product,
                        quantity=quantity,
                        price=price,
                    )
                    print(f"InvoiceDetail created: {invoice_detail}")

            invoice.invoice_total = total
            invoice.save()
            print(f"Updated Invoice: {invoice}")

        else:
            print("Formset errors: ", formset.errors)

        return redirect("invoice:invoice-payments")

   

    context = {
        'form': form,
        'formset': formset,
        
    }

    return render(request, "invoice/create_invoice.html", context)

 
#--------------------------------------------------------------------#
@login_required
def create_purchase(request):

    form = PurchaseForm()
    formset = PurchaseItemsFormSet()
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        formset = PurchaseItemsFormSet(request.POST)
        if form.is_valid():
            purchase = Purchase.objects.create(
                supplier_name=form.cleaned_data.get("supplier_name"),
                created=form.cleaned_data.get("created"),
                employee=form.cleaned_data.get("employee"),
                sub_department=form.cleaned_data.get("sub_department"),
            )
        if formset.is_valid():
            total = 0
            for form in formset:
                raw_material_name = form.cleaned_data.get("raw_material_name")
                quantity = form.cleaned_data.get("quantity")
                price = form.cleaned_data.get("price")

                if raw_material_name and quantity and price:
                    # Sum each row
                    sum = float(price) * float(quantity)
                    # Sum of total invoice
                    total += sum
                    PurchaseItems(
                        purchase=purchase,
                        raw_material_name = raw_material_name,
                        quantity=quantity,
                        price=price
                    ).save()
 
            # Save the invoice
                purchase.purchase_total = total
                purchase.save()
            return redirect("invoice:invoice-payments")

    context = {

        #"total_invoice": total_invoice,
        "form": form,
        "formset": formset,
    }

    return render(request, "invoice/create_purchase.html", context)
#--------------------------------------------------------------------#
@login_required
# Invoice view
def InvoicePayment_view(request):
        invoice = Invoice.objects.all()
        customer = Customer.objects.all()
        invoice_payments = InvoicePayment.objects.all().order_by('-date')
        #invoice_grand_total = list(invoices.aggregate(Sum('grand_total')).values())[0]

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date:
            invoice_payments = invoice_payments.filter(created__range=[start_date, end_date])
            #total_orders = list(invoices.filter(created__range=[start_date, end_date]).aggregate(Sum('amount')).values())[0]

        else:
            invoices_payments = InvoicePayment.objects.all().order_by('-date')
            #total_orders = list(invoices.aggregate(Sum('amount')).values())[0]

        template_name = 'invoice/invoice_payments.html'
        context = {
                    'invoice_payment':invoice_payments,
                    "invoice":invoice,
                    "customer":customer ,

                    }
        return render(request, template_name, context)


class add_payment_view(SuccessMessageMixin, CreateView):
    model = InvoicePayment
    template_name = 'invoice/add_payment.html'
    fields = '__all__'
    success_url = reverse_lazy("invoice:invoice-payments")
    success_message = 'Payment Transaction successful'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['invoice'].queryset = Invoice.objects.all()
        return form

    def form_invalid(self, form):
        # Debugging: Print form errors to the console
        print("Form is invalid. Errors:")
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        # Debugging: Print form data to the console
        print("Form is valid. Data:")
        print(form.cleaned_data)
        return super().form_valid(form)
# Invoice view
class edit_payment_view(SuccessMessageMixin, UpdateView):
        model = InvoicePayment
        template_name = 'invoice/edit_payment.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy("invoice:invoice-payments")
        success_message = 'Payment Transaction successfully Updated'


class add_returns_view(SuccessMessageMixin, CreateView):
        model = ReturnsItems
        template_name = 'invoice/add_returns.html'
        fields = '__all__'
        #exclude = ('slug',)
        success_url = reverse_lazy('invoice:invoice-payments')
        success_message = 'Payment Transaction successful'
 

from django.http import JsonResponse
from .models import Product  # Replace with your actual product model

def get_product_price(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.GET.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            return JsonResponse({'price': product.price})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_customer_name(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.GET.get('product_id')
        try:
            product = Invoice.objects.get(id=product_id)
            customer_name = product.customer.customer_name
            customer_id = product.customer_id
            return JsonResponse({'price': customer_name, 'id':customer_id})
        except Invoice.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


# views.py
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import InvoiceDetailFormSet  # Adjust the import based on your formset name

def add_more_row(request):
    formset = InvoiceDetailFormSet(prefix='form')
    empty_form = formset.empty_form
    rendered_row = render_to_string('invoice/new_row.html', {'form': empty_form})
    return JsonResponse({'row_html': rendered_row})
