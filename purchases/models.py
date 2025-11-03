from django.db import models
from customer.models import *
import datetime
from customer.models import *
from product.models import *
from supplier.models import *
from inventory.models import *

from django.db.models.signals import post_save
from supplier.models import *
# Create your models here.
#---------------------- Invoice Number for Invoice Model----------------------#

def increment_invoice_number():
    last_invoice = Invoices.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'PUR0001'

    invoice_id = last_invoice.invoice_id
    invoice_int = int(invoice_id.split('PUR000')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'PUR000'  + str(new_invoice_int)
    return new_invoice_id

class Invoices(models.Model):
    SubDepartment = (
        ('Boulangerie Morning', 'Boulangerie Morning'),
        ('Boulangerie Evening', 'Boulangerie Evening'),
        ('Patisserie', 'Patisserie'),
        ('Magazine', 'Magazine'),
    )
    created = models.DateField(default=now, verbose_name = "Date")
    invoice_id = models.CharField(max_length = 500, default=increment_invoice_number, null = True, blank = True, verbose_name="Purchase Invoice Id")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "supplier")
    employee =  models.CharField(max_length=200, default='', verbose_name = "Employee")
    sub_department =  models.CharField(max_length = 500, choices=SubDepartment,  default='Morning', null = True, blank = True)

    due_date = models.DateField(null=True, blank=True, verbose_name = "Due Date")


    invoice_total = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Invoice Total")
    vat_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True,)
    apply_vat = models.BooleanField(default=False)

    def __str__(self):
        return str(self.invoice_id)

    @property
    def total_amount(self):
        virtual_qty = 0
        if self.invoice_id:
            return sum([item.get_total_amount for item in self.invoicesdetail_set.all()])
        else:
            return virtual_qty

    #@property
    #def get_total_returns(self):
        #virtual_qty = 0
        #if self.invoice_id:
            #return sum([item.total_return_amount for item in self.returnsitems_set.all()])
        #else:
            #return virtual_qty

    @property
    def get_grand_total(self):
        virtual_qty = 0
        if self.invoice_id:
            return sum([item.get_total_amount for item in self.invoicesdetail_set.all()]) + self.vat_amount
        else:
            return virtual_qty

    @property
    def total_amount_paid(self):
        virtual_amount = 0
        if self.invoice_id:
            return sum([item.get_total_amount_paid for item in self.purchaseinvoicespayment_set.all()])
        else:
            return virtual_amount


    @property
    def balance_due(self):
        virtual_amount = 0
        if self.get_grand_total and self.total_amount_paid:
            return self.get_grand_total - self.total_amount_paid
        elif not self.total_amount_paid:
            return self.get_grand_total
        elif not self.get_grand_total and not self.total_amount_paid:
            return virtual_amount
        else:
            return virtual_amount




    def save(self, *args, **kwargs):
        if not self.id:
            #self.due_date = datetime.datetime.now()+ datetime.timedelta(days=3)
            self.due_date = self.created + datetime.timedelta(days=3)

        return super(Invoices, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Purchase Invoice'
        verbose_name_plural = 'Purchase Invoices'


class InvoicesDetail(models.Model):

    invoice = models.ForeignKey(Invoices, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Invoice Id")
    product = models.ForeignKey(RawMaterials, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Raw Material")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    discount_price = models.DecimalField(max_digits=10, blank=True, null=True, default=0,decimal_places=2)
    discount_value = models.FloatField(blank=True, null=True, default=0)
    net_amount = models.DecimalField(max_digits=10, blank=True, null=True, default=0, decimal_places=2)

    @property
    def get_total_amount(self):
        total = (Decimal(self.quantity) * Decimal(self.price))
        return total

    class Meta:
        verbose_name = 'Purchase Invoice Items'
        verbose_name_plural = 'Purchase Invoice Items'

# Overriding the save method to update invoice total for each new item
    def save(self, *args, **kwargs):
        self.total = (Decimal(self.quantity) * Decimal(self.price))
        #self.total_amount = order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
        #self.invoice.save()
        super().save(*args, **kwargs)
#-----------------------------------------------------------------------------#

def increment_invoice_number():
    last_invoice_payment = PurchaseInvoicesPayment.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice_payment:
            return today_string + "-" + 'PAYMT0001'

    payment_id = last_invoice_payment.payment_id
    payment_int = int(payment_id.split('PAYMT000')[-1])
    new_payment_int = payment_int + 1

    new_payment_id = today_string + "-" + 'PAYMT000'  + str(new_payment_int)
    return new_payment_id

class PurchaseInvoicesPayment(models.Model):
    Payment_Installment = (
        ('1st Installment', '1st Installment'),
        ('2nd Installment', '2nd Installment'),
        ('3rd Installment', '3rd Installment'),
        ('4th Installment', '4th Installment'),
        ('5th Installment', '5th Installment'),
        ('6th Installment', '6th Installment'),
        ('7th Installment', '7th Installment'),
        ('8th Installment', '8th Installment'),
        ('9th Installment', '9th Installment'),
        ('10th Installment', '10th Installment'),

    )

    date = models.DateField(default=now)
    invoice = models.ForeignKey(Invoices, on_delete=models.SET_NULL, null = True, blank = True, default='')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    payment_installment =  models.CharField(max_length = 500, choices=Payment_Installment,  default='1st Installment', null = True, blank = True)
    employee = models.CharField(max_length = 500, null = True, blank = True, default='')
    amount_paid = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    payment_id = models.CharField(max_length = 500,default=increment_invoice_number, null = True, blank = True)

    def __str__(self):
        return self.payment_id

    @property
    def get_total_amount_paid(self):
        virtual_amount = 0
        if self.invoice_id:
            return self.amount_paid
        else:
            return virtual_amount

    class Meta():
        verbose_name = 'Purchase Invoice Payments'
        verbose_name_plural = 'Purchase Invoice Payments'

#def payment_signal(sender, **kwargs):
    #if kwargs['created']:
        #payment_signal_trans = InvoicePayment.objects.create(invoice=kwargs['instance'])

#post_save.connect(payment_signal, sender=Invoice)

# Create your models here.
#------------------------------------------------------------------------------------------------#
'''
def increment_purchase_number():
    last_invoice = Purchase.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'PUR001'

    invoice_id = last_invoice.purchase_id
    invoice_int = int(invoice_id.split('PUR00')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'PUR00'  + str(new_invoice_int)
    return new_invoice_id
#------------------------------------------------------------------------------------------------#

class Purchase(models.Model):
    SubDepartment = (
        ('Boulangerie Morning', 'Boulangerie Morning'),
        ('Boulangerie Evening', 'Boulangerie Evening'),
        ('Patisserie', 'Patisserie'),
        ('Magazine', 'Magazine'),
    )
    created = models.DateField(default=now, verbose_name = "Date")
    purchase_id = models.CharField(max_length = 500,default=increment_purchase_number, null = True, blank = True, verbose_name="Customer Name")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    supplier_name = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Supplier's Name")
    sub_department =  models.CharField(max_length = 500, choices=SubDepartment,  default='Morning', null = True, blank = True)
    due_date = models.DateField(null=True, blank=True, verbose_name = "Due Date")
    purchase_total = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Purchase Total")

    def __str__(self):
        return str(self.sub_department)

    class Meta():
        verbose_name = 'Purchase Invoice'
        verbose_name_plural = 'Purchase Invoice'

#------------------------------------------------------------------------------------------------#
class PurchaseItems(models.Model):
    purchase_id = models.ForeignKey(Purchase, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Purchase Id")
    raw_material_name = models.ForeignKey(RawMaterials, related_name="raw_material_purchase", on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True,)

    class Meta():
        verbose_name = 'Purchase Item'
        verbose_name_plural = 'Purchase Items'

    # Overriding the save method to update invoice total for each new item
    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        #self.total_amount = order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
        #self.invoice.save()
        super().save(*args, **kwargs)
#------------------------------------------------------------------------------------------------#

class ReturnsItems(models.Model):
    Sales_Session = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    )

    date = models.DateField(default=now)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    sales_person =  models.CharField(max_length=200, default='', verbose_name = "Sale Person")
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Invoice Id")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True)
    total = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True)

    @property
    def total_return_amount(self):
        return (Decimal(self.quantity) * Decimal(self.price))

    def save(self, *args, **kwargs):
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Customers Return Item'
        verbose_name_plural = 'Customers Return Items'
'''
