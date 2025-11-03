from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from django.urls import reverse_lazy

from django.core.paginator import Paginator

from django.db.models import Sum
from django.db.models import Q

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from . models import *
from . forms import *
# Create your views here. 
@login_required
def customer(request):
    customers = Customer.objects.all()

    template_name = 'customer/customers.html'
    context = {'customers':customers}
    return render(request, template_name, context)
#-------------------------------------------------------------------------#
class add_customer(SuccessMessageMixin, CreateView):
    model = Customer
    template_name = 'customer/forms/add_customer.html'
    fields = '__all__'
    exclude = ('slug',)
    success_url = reverse_lazy('customer:customer')
    success_message = 'Customer Account Successfully Created !!!'
 
#------------------------------------------ -------------------------------#
class edit_customer(SuccessMessageMixin, UpdateView):
    model = Customer
    template_name = 'customer/forms/edit_customer.html'
    fields = '__all__'
    exclude = ('slug',)
    success_url = reverse_lazy('customer:customer')
    success_message = 'Customer Account Successfully Edited !!!'
#-------------------------------------------------------------------------# 
@login_required
def customer_details(request, slug):
    customers = Customer.objects.get(slug=slug)
    #opening_balance = customers.customeropeningbalance_set.all()
    invoice = customers.invoice_set.all()
    invoice_total = list(invoice.aggregate(Sum('invoice_total')).values())[0]


    #returns = customers.returnsitems_set.all()
    #returns_total = list(returns.aggregate(Sum('total')).values())[0]


    payments = customers.invoicepayment_set.all()
    payment_total = list(payments.aggregate(Sum('amount_paid')).values())[0]

    template_name = 'customer/customer_account.html'
    context = {'customers':customers,
                #'opening_balance':opening_balance,
                'invoice':invoice,

                'payments':payments,
                'payment_total': payment_total,

                'invoice_total':invoice_total,


                #'returns':returns,
                #'returns_total':returns_total

                }

    return render(request, template_name, context)
