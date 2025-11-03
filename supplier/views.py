from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from django.urls import reverse_lazy

from django.core.paginator import Paginator

from django.db.models import Sum
from django.db.models import Q

from django.core.paginator import Paginator

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from . models import *
from purchases.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def suppliers_view(request):
    suppliers = Supplier.objects.all()

    template_name = 'supplier/suppliers.html'
    context = {'suppliers':suppliers}
    return render(request, template_name, context)
#-------------------------------------------------------------------#
@login_required
def supplier_details(request, slug):#
    supplier = Supplier.objects.get(slug=slug)

    supplier_invoice = supplier.invoices_set.all()
    supplier_invoice_total = list(supplier_invoice.aggregate(Sum('invoice_total')).values())[0]

    #opening_balance = customers.customeropeningbalance_set.all()
    #returns = customers.returnsitems_set.all()
    #returns_total = list(returns.aggregate(Sum('total')).values())[0]


    purchase_payments =supplier.purchaseinvoicespayment_set.all()
    total_purchase_payment= list(purchase_payments.aggregate(Sum('amount_paid')).values())[0]

    template_name = 'supplier/supplier_account.html'
    context = {'supplier':supplier,
                #'opening_balance':opening_balance,
                'supplier_invoice':supplier_invoice,
                'supplier_invoice_total':supplier_invoice_total,

                'purchase_payments':purchase_payments,
                'total_purchase_payment':total_purchase_payment,
                }
 
    return render(request, template_name, context)
#-------------------------------------------------------------------------#
class add_supplier(SuccessMessageMixin, CreateView):
    model = Supplier
    template_name = 'supplier/forms/add_supplier.html'
    fields = '__all__'
    exclude = ('slug',)
    success_url = reverse_lazy('supplier:supplier')
    success_message = 'supplier Account Successfully Created !!!'

#-------------------------------------------------------------------------#
class edit_supplier(SuccessMessageMixin, UpdateView):
    model = Supplier
    template_name = 'supplier/forms/edit_supplier.html'
    fields = '__all__'
    exclude = ('slug',)
    success_url = reverse_lazy('supplier:supplier')
    success_message = 'supplier Account Successfully Edited !!!'
#-------------------------------------------------------------------------#
