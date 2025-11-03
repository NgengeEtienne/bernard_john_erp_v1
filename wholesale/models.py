from django.db import models
from django.template.defaultfilters import slugify
import datetime
from datetime import datetime, timedelta,date
from decimal import Decimal
from django.urls import reverse
from django.utils.timezone import now
from configuration.models import *
from django.core.validators import RegexValidator, MinValueValidator
import uuid
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Sum




#############   #############   #############   #############   #############
#------------------------- Product / Category ------------------------------#
#############   #############   #############   #############   #############
 
'''
class WholesaleProductCategory(models.Model):
    category_name = models.CharField(max_length=100, default='', verbose_name = "Category Name")
    sub_department = models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, null=True, blank =True, verbose_name = "Sub Department")


    def __str__(self):
        return str(self.category_name)

    class Meta:
        verbose_name = 'Wholesale Product Category'
        verbose_name_plural = 'Wholesale Product Category'
'''
class WholesaleProductSubCategory(models.Model):
    sub_category_name = models.CharField(max_length=100, default='', verbose_name = "Sub Category Name")
    #category_name = models.ForeignKey(WholesaleProductCategory, on_delete=models.SET_NULL, null=True, blank =True, verbose_name = "Category")


    def __str__(self):
        return str(self.sub_category_name)

    class Meta:
        verbose_name = 'Wholesale Product Sub Category'
        verbose_name_plural = 'Wholesale Product Sub Category'


class WholesaleProduct(models.Model):
    product_name = models.CharField(max_length=100, default='', unique=True, verbose_name = "Product Name")
    sub_category_name = models.ForeignKey(WholesaleProductSubCategory, on_delete=models.SET_NULL, default=1, null = True, blank = True, verbose_name = "Category")
    barcode= models.CharField(max_length=100, default="", null = True, blank = True, verbose_name = "Barcode",)
    cost_price = models.DecimalField(max_digits=20, decimal_places=2, null = True, blank = True, default=0, verbose_name = "Cost Price")
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True, verbose_name = "Selling Price")
    reorder_level = models.DecimalField(max_digits=20, decimal_places=2, null = True, blank = True, default=0, verbose_name = "Reorder Level")
    #slug = models.SlugField(max_length=100, unique=True, blank=True)


    def __str__(self):
        return str(self.product_name)

    class Meta:
        verbose_name = 'Wholesale Product'
        verbose_name_plural = 'Wholesale Products'


#############   #############   #############   #############   #############
    #------------------------- Customer --------------------------------#
#############   #############   #############   #############   #############

from django.db.models.signals import post_save
# Create your models here.
#---------------------- Invoice Number for Invoice Model----------------------#

# Create your models here.

# phone validator using regular expressions
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message='Phone number invalid. Should start with example: +237'
)

class WholesaleCustomer(models.Model):

    Customer_TYPE = (
        ('Supplier', 'Supplier'),
        ('Sole Proprietor', 'Sole Proprietor'),
        ('Customer', 'Customer'),
        ('Company', 'Company'),
        ('Enterprise', 'Enterprise'),
        ('Individual', 'Individual'),
        ('School', 'School'),
        ('NGOs', 'NGOs'),
    )
    Company_box = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    Street_Location = (
        ('Along the Road', 'Along the Road'),
        ('Inside the Street', 'Inside the Street'),
    )
    #General information fields
    customer_name = models.CharField(max_length=200, default='Defualt Customer', unique=True,  verbose_name = "Customer Name")
    customer_type = models.CharField(max_length=100, choices=Customer_TYPE , null = True, blank = True, verbose_name = "Customer Type")
    company_name = models.CharField(max_length=200, default='', null = True, blank = True, verbose_name = "Company Name")
    company_box = models.CharField(max_length=100, choices=Company_box, null = True, blank = True, verbose_name = "Own Company Box")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    #Contact details fields
    area = models.CharField(max_length=255,  null = True, blank = True, verbose_name = "Area")
    quarter = models.CharField(max_length=255, null=True,blank = True, verbose_name = "Quarter")
    street = models.CharField(max_length=255, null=True,blank = True, verbose_name = "Street")
    street_location = models.CharField(max_length=30, choices=Street_Location, null = True, blank = True, verbose_name = "Street Location")
    address = models.TextField(max_length=2550, null=True, verbose_name = "Address")
    city = models.CharField(max_length=100, default='Kumba', verbose_name = "City")
    region = models.CharField(max_length=200, default='South West Region', verbose_name = "Region")
    phone = models.CharField(validators=[phone_regex], max_length=15, null=True, blank = True, verbose_name = "Phone +237")
    email = models.EmailField(blank=True, null=True, verbose_name = "Email")
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'Wholesale Customer'
        verbose_name_plural = 'Wholesale Customers'

    def __str__(self):
        return "{}".format(self.customer_name)


    def get_absolute_url(self):
        return reverse('customer:customer-details', args=[self.slug])

    def save(self, *args, **kwargs):
            self.slug = slugify(self.customer_name)
            super(WholesaleCustomer, self).save(*args, **kwargs)

    #class Meta:
        #ordering = ['-created']



#############   #############   #############   #############   #############
    #------------------------- Invoicing --------------------------------#
#############   #############   #############   #############   #############

def Wholesale_increment_invoice_number():
    last_invoice = WholesaleInvoice.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'WHSINV0001'

    invoice_id = last_invoice.invoice_id
    invoice_int = int(invoice_id.split('WHSINV000')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'WHSINV000'  + str(new_invoice_int)
    return new_invoice_id

#############   #############   #############   #############   #############
    #------------------------- Invoicing --------------------------------#
#############   #############   #############   #############   #############

class WholesaleInvoice(models.Model):

    Status = (
        ('Sales', 'Sales'),
        ('Return Inwards', 'Return Inwards'),
    )
    created = models.DateField(default=now, verbose_name = "Date")
    # department_name =  models.ForeignKey(Department, on_delete=models.SET_NULL, null = True, blank = True, verbose_name = 'Department')
    invoice_id = models.CharField(max_length = 500, default=Wholesale_increment_invoice_number, null = True, blank = True, verbose_name="Invoice Id")
    customer = models.ForeignKey(WholesaleCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    status =  models.CharField(max_length = 500, choices=Status,  default='Morning', null = True, blank = True)
    due_date = models.DateField(null=True, blank=True, verbose_name = "Due Date")
    invoice_total = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Invoice Total")


    def __str__(self):
        return str(self.invoice_id)

    # @property
    # def total_amount(self):
    #     virtual_qty = 0
    #     if self.invoice_id:
    #         return sum([item.get_total_amount for item in self.wholesaleinvoicedetail_set.all()])
    #     else:
    #         return virtual_qty

    # @property
    # def get_total_returns(self):
    #     virtual_qty = 0
    #     if self.invoice_id:
    #         return sum([item.total_return_amount for item in self.wholesalereturnsitems_set.all()])
    #     else:
    #         return virtual_qty

    # @property
    # def get_grand_total(self):
    #     virtual_qty = 0
    #     if self.invoice_id:
    #         return sum([item.get_total_amount for item in self.wholesaleinvoicedetail_set.all()])
    #     else:
    #         return virtual_qty
 
    @property
    def total_amount_paid(self):
        virtual_amount = 0
        if self.invoice_id:
            return sum([item.get_total_amount_paid for item in self.wholesaleinvoicepayment_set.all()])
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
                year, month, day = map(int, self.created.split('-'))
                created_date = date(year, month, day)

                # Add 3 days
                due_date = created_date + timedelta(days=3)

                # Store due_date as a string again
                self.due_date = due_date.isoformat() 

        return super(WholesaleInvoice, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Wholesale Customer Invoice'
        verbose_name_plural = 'Wholesale Customer Invoice'


class WholesaleInvoiceDetail(models.Model):
    sales_person =  models.CharField(max_length=200, default='', verbose_name = "Sale Person")
    invoice = models.ForeignKey(WholesaleInvoice, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Invoice Id")
    delivery_man =  models.CharField(max_length=200, default='', verbose_name = "Delivery Man")
    product = models.ForeignKey(WholesaleProduct, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    unit_cost_price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    unit_selling_price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    total_cost_price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    total_selling_price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    discount_price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    discount_value = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    net_amount = models.DecimalField(max_digits=20, decimal_places=0, default=0)

    #@property
    #def get_total_amount(self):
        #total = (Decimal(self.quantity) * Decimal(self.price))
        #return total
    def __str__(self):
        return str(self.sales_person)

    class Meta:
        verbose_name = 'Wholesale Customer InvoicedItems'
        verbose_name_plural = 'Wholesale Customer InvoicedItems'

# Overriding the save method to update invoice total for each new item
# from decimal import Decimal

    def save(self, *args, **kwargs):
        # Convert all values to Decimal
        unit_cost_price = Decimal(self.unit_cost_price)
        unit_selling_price = Decimal(self.unit_selling_price)
        discount_price = Decimal(self.discount_price)
        quantity = Decimal(self.quantity)
        
        # Perform calculations with Decimal
        self.total_cost_price = quantity * unit_cost_price
        self.total_selling_price = quantity * unit_selling_price
        self.discount_value = quantity * discount_price
        
        # Ensure net_amount calculation uses Decimal
        self.net_amount = self.total_selling_price - self.discount_value
        
        super().save(*args, **kwargs)



def increment_invoice_number():
    last_invoice_payment = WholesaleInvoicePayment.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice_payment:
            return today_string + "-" + 'BAKPAYMT0001'

    payment_id = last_invoice_payment.payment_id
    payment_int = int(payment_id.split('BAKPAYMT000')[-1])
    new_payment_int = payment_int + 1

    new_payment_id = today_string + "-" + 'BAKPAYMT000'  + str(new_payment_int)
    return new_payment_id


#############   #############   #############   #############   #############
#------------------------- Wholesale Payment ---------------------#
#############   #############   #############   #############   #############
class WholesaleInvoicePayment(models.Model):
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
    invoice = models.ForeignKey(WholesaleInvoice, on_delete=models.SET_NULL, null = True, blank = True,)
    #payment_id = models.CharField(max_length = 500,default=increment_invoice_number, null = True, blank = True)
    customer = models.ForeignKey(WholesaleCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    payment_installment =  models.CharField(max_length = 500, choices=Payment_Installment,  default='1st Installment', null = True, blank = True)
    employee = models.CharField(max_length = 500, null = True, blank = True, default='')
    amount_paid = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    

    def __str__(self):
        return self.payment_installment

    @property
    def get_total_amount_paid(self):
        return self.amount_paid

    class Meta():
        verbose_name = 'Wholesale Customers Payments'
        verbose_name_plural = 'Wholesale Customers Payments'
        
        
        
        
        
        
class WholesaleOpeningBalance(models.Model):
    Sales_Session = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    )

    date = models.DateField(default=now)
    customer = models.ForeignKey(WholesaleCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    #sales_person =  models.CharField(max_length=200, default='', verbose_name = "Sale Person")
    invoice = models.ForeignKey(WholesaleInvoice, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Invoice Id")
    product = models.ForeignKey(WholesaleProduct, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
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
        verbose_name = 'Customers Opening Balance'
        verbose_name_plural = 'Customers Opening Balance'

#-----------------------------------------------------------------#

#############   #############   #############   #############   #############
#------------------------- Wholesale Supplier ---------------------#
#############   #############   #############   #############   #############

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message='Phone number invalid. Should start with example: +237'
)

class WholesaleSupplier(models.Model):

    Supplier_TYPE = (

        ('Company', 'Company'),
        ('Enterprise', 'Enterprise'),
        ('Individual', 'Individual'),

    )

    #General information fields
    supplier_name = models.CharField(max_length=200,  verbose_name = "Supplier Name")
    supplier_type = models.CharField(max_length=100, choices=Supplier_TYPE , null = True, blank = True, verbose_name = "Supplier Type")
    company_name = models.CharField(max_length=200, default='', null = True, blank = True, verbose_name = "Company Name")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    #Contact details fields
    address = models.TextField(max_length=2550, null = True, blank = True, verbose_name = "Address")
    city = models.CharField(max_length=100, default='Kumba', null = True, blank = True, verbose_name = "City")
    region = models.CharField(max_length=200, default='South West Region', null = True, blank = True, verbose_name = "Region")
    phone1 = models.CharField(validators=[phone_regex], max_length=15, null=True, blank = True, verbose_name = "Phone 1 +237")
    phone2 = models.CharField(validators=[phone_regex], max_length=15, null=True, blank = True, verbose_name = "Phone 2 +237")
    email = models.EmailField(blank=True, null=True, verbose_name = "Email")

    class Meta:
        verbose_name = ' Wholesale Suppliers'
        verbose_name_plural = 'Wholesale Suppliers'

    def __str__(self):
        return "{}".format(self.supplier_name)


    def get_absolute_url(self):
        return reverse('supplier:supplier-details', args=[self.slug])

    def save(self, *args, **kwargs):
            self.slug = slugify(self.supplier_name)
            super(WholesaleSupplier, self).save(*args, **kwargs)

    #class Meta:
        #ordering = ['-created']

#----------------------------------Purchase Summary ---------------------------------------------#
#------------------------------------------------------------------------------------------------#
class WholesalePurchaseSummary(models.Model):
    SubDepartment = (
        ('Boulangerie Morning', 'Boulangerie Morning'),
        ('Boulangerie Evening', 'Boulangerie Evening'),
        ('Patisserie', 'Patisserie'),
        ('Magazine', 'Magazine'),
    )
    created = models.DateField(default=now, verbose_name = "Date")
    purchase_id = models.CharField(max_length = 500,default='', null = True, blank = True, verbose_name="Purchase ID")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    supplier_name = models.ForeignKey(WholesaleSupplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Supplier's Name")
    description = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="Description")
    purchase_value = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Purchase Value")
    amount_paid = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Amount Paid")
    balance_due = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Balance Due")
    due_date = models.DateField(null=True, blank=True, verbose_name = "Due Date")

    def __str__(self):
        return str(self.purchase_id)
      
    def save(self, *args, **kwargs):
        if not self.id:
            #self.due_date = datetime.datetime.now()+ datetime.timedelta(days=3)
            self.balance_due = self.purchase_value - self.amount_paid
            self.due_date = self.created + datetime.timedelta(days=3)

        return super(WholesalePurchaseSummary, self).save(*args, **kwargs)


    class Meta():
        verbose_name = 'Wholesale Purchase Summary'
        verbose_name_plural = 'Wholesale Purchase Summary'
#----------------------------------Purchase Summary ---------------------------------------------#



    
#############   #############   #############   #############   #############
#---------------------------- Wholesale Raw Materials -------------------------#
#############   #############   #############   #############   #############
    
def increment_purchase_number():
    last_invoice = WholesalePurchase.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'SUPPUR001'

    invoice_id = last_invoice.purchase_id
    invoice_int = int(invoice_id.split('SUPPUR00')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'SUPPUR00'  + str(new_invoice_int)
    return new_invoice_id


class WholesalePurchase(models.Model):
    SubDepartment = (
        ('Boulangerie Morning', 'Boulangerie Morning'),
        ('Boulangerie Evening', 'Boulangerie Evening'),
        ('Patisserie', 'Patisserie'),
        ('Magazine', 'Magazine'),
    )
    Status = (
        ('Purchases', 'Purchases'),
        ('Return Outwards', 'Return Outwards'),
       
    )
    created = models.DateField(default=now, verbose_name = "Date")
    purchase_id = models.CharField(max_length = 500,default=increment_purchase_number, null = True, blank = True, verbose_name="Customer Name")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    supplier_name = models.ForeignKey(WholesaleSupplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Supplier's Name")
    # sub_department =  models.CharField(max_length = 500, choices=SubDepartment,  default='Morning', null = True, blank = True)
    status =  models.CharField(max_length = 500, choices=Status,  default='Purchases', null = True, blank = True)
    due_date = models.DateField(null=True, blank=True, verbose_name = "Due Date")
    purchase_total = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Purchase Total")
    net_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Net Amount")

    def __str__(self):
        return str(self.purchase_id)
    
    def save(self, *args, **kwargs):
        if not self.id:
            year, month, day = map(int, self.created.split('-'))
            created_date = date(year, month, day)

            # Add 3 days
            self.due_date = created_date + timedelta(days=3)
            # self.net_amount = self.purchase_total - self.discount_amount + self.vat_amount

        return super(WholesalePurchase, self).save(*args, **kwargs)

    class Meta():
        verbose_name = 'Wholesale Purchase Invoice'
        verbose_name_plural = 'Wholesale Purchase Invoice'



class WholesalePurchaseItems(models.Model):
    purchase_id = models.ForeignKey(WholesalePurchase, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Purchase Id")
    product = models.ForeignKey(WholesaleProduct, related_name="raw_material_purchase", on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True,)
    discount_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Discount price")
    discount_value = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Discount Amount")
   
    class Meta():
        verbose_name = 'Wholesale Purchase Item'
        verbose_name_plural = 'Wholesale Purchase Items'

    # Overriding the save method to update invoice total for each new item
    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        self.discount_value = self.discount_amount * self.quantity
        #self.invoice.save()
        super().save(*args, **kwargs)
#------------------------------------------------------------------------------------------------#
###########   #############   #############   #############   #############
#---------------------------- Wholesale Inventory -------------------------#
#############   #############   #############   #############   #############


        
'''
#############   #############   #############   #############   #############
    #------------------------- Invoicing --------------------------------#
#############   #############   #############   #############   #############
def opening_bal_increment_invoice_number():
    last_invoice_payment = WholesaleCustomerOpeningBalance.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice_payment:
            return today_string + "-" + 'BAKCUSTOB0001'

    payment_id = last_invoice_payment.payment_id
    payment_int = int(payment_id.split('BAKCUSTOB000')[-1])
    new_payment_int = payment_int + 1

    new_payment_id = today_string + "-" + 'BAKCUSTOB000'  + str(new_payment_int)
    return new_payment_id

class WholesaleCustomerOpeningBalance(models.Model):
    Opening_bal_des = (
        ('Opening Balance', 'Opening Balance'),
    )

    date = models.DateField(default=now)
    invoice = models.ForeignKey(WholesaleInvoice, on_delete=models.SET_NULL, null = True, blank = True,)
    #opening_bal_id = models.CharField(max_length = 500,default=opening_bal_increment_invoice_number, null = True, blank = True, verbose_name = "Customer Name")
    customer = models.ForeignKey(WholesaleCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    description =  models.CharField(max_length = 500, choices=Opening_bal_des,  default='Customer Opening Balance', null = True, blank = True, verbose_name = "Description")
    amount_owed = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    

    def __str__(self):
        return self.opening_bal_id

    class Meta:
        verbose_name = 'Wholesale Customer Opening Balance'
        verbose_name_plural = 'Wholesale Customer Opening Balance'    
        
#-----------------------------------------------------------------------------#
#############   #############   #############   #############   #############
    #------------------------- Payments --------------------------------#
#############   #############   #############   #############   #############
def increment_invoice_number():
    last_invoice_payment = WholesaleInvoicePayment.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice_payment:
            return today_string + "-" + 'BAKPAYMT0001'

    payment_id = last_invoice_payment.payment_id
    payment_int = int(payment_id.split('BAKPAYMT000')[-1])
    new_payment_int = payment_int + 1

    new_payment_id = today_string + "-" + 'BAKPAYMT000'  + str(new_payment_int)
    return new_payment_id

class WholesaleInvoicePayment(models.Model):
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
    invoice = models.ForeignKey(WholesaleInvoice, on_delete=models.SET_NULL, null = True, blank = True,)
    #payment_id = models.CharField(max_length = 500,default=increment_invoice_number, null = True, blank = True)
    customer = models.ForeignKey(WholesaleCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    payment_installment =  models.CharField(max_length = 500, choices=Payment_Installment,  default='1st Installment', null = True, blank = True)
    employee = models.CharField(max_length = 500, null = True, blank = True, default='')
    amount_paid = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    

    def __str__(self):
        return self.payment_installment

    @property
    def get_total_amount_paid(self):
        return self.amount_paid

    class Meta():
        verbose_name = 'Wholesale Customers Payments'
        verbose_name_plural = 'Wholesale Customers Payments'



#------------------------------------------------------------------------------------------------#
#----------------------------------- Wholesale Return Items ----------------------------------------#
#------------------------------------------------------------------------------------------------#
class WholesaleReturnsItems(models.Model):
    Sales_Session = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    )

    date = models.DateField(default=now)
    customer = models.ForeignKey(WholesaleCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    #sales_person =  models.CharField(max_length=200, default='', verbose_name = "Sale Person")
    invoice = models.ForeignKey(WholesaleInvoice, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Invoice Id")
    product = models.ForeignKey(WholesaleProduct, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
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

#-----------------------------------------------------------------#
#------------------------------------------------------------------------------------------------#
#############   #############   #############   #############   #############
#------------------------- Wholesale Supplier ---------------------#
#############   #############   #############   #############   #############

phone_regex = RegexValidator(
    
    message='Phone number invalid. Should start with example: +237'
)

class WholesaleSupplier(models.Model):

    Supplier_TYPE = (

        ('Company', 'Company'),
        ('Enterprise', 'Enterprise'),
        ('Individual', 'Individual'),

    )

    #General information fields
    supplier_name = models.CharField(max_length=200,  verbose_name = "Supplier Name")
    supplier_type = models.CharField(max_length=100, choices=Supplier_TYPE , null = True, blank = True, verbose_name = "Supplier Type")
    company_name = models.CharField(max_length=200, default='', null = True, blank = True, verbose_name = "Company Name")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    #Contact details fields
    address = models.TextField(max_length=2550, null = True, blank = True, verbose_name = "Address")
    city = models.CharField(max_length=100, default='Kumba', null = True, blank = True, verbose_name = "City")
    region = models.CharField(max_length=200, default='South West Region', null = True, blank = True, verbose_name = "Region")
    phone1 = models.CharField(validators=[phone_regex], max_length=15, null=True, blank = True, verbose_name = "Phone 1 +237")
    phone2 = models.CharField(validators=[phone_regex], max_length=15, null=True, blank = True, verbose_name = "Phone 2 +237")
    email = models.EmailField(blank=True, null=True, verbose_name = "Email")

    class Meta:
        verbose_name = ' Wholesale Suppliers'
        verbose_name_plural = 'Wholesale Suppliers'

    def __str__(self):
        return "{}".format(self.supplier_name)


    def get_absolute_url(self):
        return reverse('supplier:supplier-details', args=[self.slug])

    def save(self, *args, **kwargs):
            self.slug = slugify(self.supplier_name)
            super(WholesaleSupplier, self).save(*args, **kwargs)

    #class Meta:
        #ordering = ['-created']

#----------------------------------Purchase Summary ---------------------------------------------#
#------------------------------------------------------------------------------------------------#
class WholesalePurchaseSummary(models.Model):
    SubDepartment = (
        ('Boulangerie Morning', 'Boulangerie Morning'),
        ('Boulangerie Evening', 'Boulangerie Evening'),
        ('Patisserie', 'Patisserie'),
        ('Magazine', 'Magazine'),
    )
    created = models.DateField(default=now, verbose_name = "Date")
    purchase_id = models.CharField(max_length = 500,default='', null = True, blank = True, verbose_name="Purchase ID")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    supplier_name = models.ForeignKey(WholesaleSupplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Supplier's Name")
    description = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="Description")
    purchase_value = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Purchase Value")
    amount_paid = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Amount Paid")
    balance_due = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Balance Due")
    due_date = models.DateField(null=True, blank=True, verbose_name = "Due Date")

    def __str__(self):
        return str(self.purchase_id)
      
    def save(self, *args, **kwargs):
        if not self.id:
            #self.due_date = datetime.datetime.now()+ datetime.timedelta(days=3)
            self.balance_due = self.purchase_value - self.amount_paid
            self.due_date = self.created + datetime.timedelta(days=3)

        return super(WholesalePurchaseSummary, self).save(*args, **kwargs)


    class Meta():
        verbose_name = 'Wholesale Purchase Summary'
        verbose_name_plural = 'Wholesale Purchase Summary'
#----------------------------------Purchase Summary ---------------------------------------------#

#############   #############   #############   #############   #############
#---------------------------- Wholesale Raw Materials -------------------------#
#############   #############   #############   #############   #############

class RawMaterials(models.Model):
    CATEGORY = (
        ('Direct', 'Direct'),
        ('Indirect', 'Indirect'),
        ('Semifinished Boulangerie', 'Semifinished Boulangerie'),
        ('Semifinished Patisserie', 'Semifinished Patisserie'),
        ('Finished Boulangerie', 'Finished Boulangerie'),
        ('Finished Patisserie', 'Finished Patisser')
    )

    ENTRYMEASURE = (
        ('Grams', 'Grams'),
        ('Kg', 'Kg'),
        ('Unit', 'Unit'),
        ('Litre', 'Litre'),

    )

    PACKAGING = (
        ('Bags', 'Bags'),
        ('Packets', 'Packets'),
        ('Bottle', 'Bottle'),
        ('Sachets', 'Sachets'),
        ('Buckets', 'Buckets'),
        ('Litre', 'Litre'),
        ('Trays', 'Trays'),
        ('Carton', 'Carton'),
        ('Container', 'Container'),

    )

    TAG = (
        ('Raw Material', 'Raw Material'),
        ('Semi Finished Product', 'Semi Finished Product'),
        ('Finished Product', 'Finished Product'),
    )

    raw_material_name =  models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name = 'Raw Material')
    category=  models.CharField(max_length = 500, choices=CATEGORY, default='Direct', null = True, blank = True, verbose_name = 'Category')
    weight_pack =   models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank=True, verbose_name = 'Weight/Pack')
    entry_measure =  models.CharField(max_length=200, choices=ENTRYMEASURE, verbose_name = 'Entry Measure')
    tag =  models.CharField(max_length=200, choices=TAG, default='', verbose_name = 'Product Tag')
    packaging =  models.CharField(max_length = 500, default='', choices=PACKAGING, null = True, blank = True, verbose_name = 'Packaging')


    def __str__(self):
        return self.raw_material_name

    class Meta():
        verbose_name = 'Raw Material'
        verbose_name_plural = 'Raw Material'

    
#############   #############   #############   #############   #############
#---------------------------- Wholesale Raw Materials -------------------------#
#############   #############   #############   #############   #############
    
def increment_purchase_number():
    last_invoice = WholesalePurchase.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'BAKPUR001'

    invoice_id = last_invoice.purchase_id
    invoice_int = int(invoice_id.split('BAKPUR00')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'BAKPUR00'  + str(new_invoice_int)
    return new_invoice_id


class WholesalePurchase(models.Model):
    SubDepartment = (
        ('Boulangerie Morning', 'Boulangerie Morning'),
        ('Boulangerie Evening', 'Boulangerie Evening'),
        ('Patisserie', 'Patisserie'),
        ('Magazine', 'Magazine'),
    )
    created = models.DateField(default=now, verbose_name = "Date")
    purchase_id = models.CharField(max_length = 500,default=increment_purchase_number, null = True, blank = True, verbose_name="Customer Name")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    supplier_name = models.ForeignKey(WholesaleSupplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Supplier's Name")
    #sub_department =  models.CharField(max_length = 500, choices=SubDepartment,  default='Morning', null = True, blank = True)
    due_date = models.DateField(null=True, blank=True, verbose_name = "Due Date")
    purchase_total = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Purchase Total")
    vat_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="VAT Amount")
    discount_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Discount Amount")
    net_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Net Amount")

    def __str__(self):
        return str(self.purchase_id)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.due_date = self.created + datetime.timedelta(days=3)
            self.net_amount = self.purchase_total - self.discount_amount + self.vat_amount

        return super(WholesalePurchase, self).save(*args, **kwargs)

    class Meta():
        verbose_name = 'Wholesale Purchase Invoice'
        verbose_name_plural = 'Wholesale Purchase Invoice'



class WholesalePurchaseItems(models.Model):
    purchase_id = models.ForeignKey(WholesalePurchase, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Purchase Id")
    raw_material_name = models.ForeignKey(RawMaterials, related_name="raw_material_purchase", on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True,)

    class Meta():
        verbose_name = 'Wholesale Purchase Item'
        verbose_name_plural = 'Wholesale Purchase Items'

    # Overriding the save method to update invoice total for each new item
    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        #self.total_amount = order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
        #self.invoice.save()
        super().save(*args, **kwargs)
#------------------------------------------------------------------------------------------------#
###########   #############   #############   #############   #############
#---------------------------- Wholesale Inventory -------------------------#
#############   #############   #############   #############   #############

def increment_inventory_number():
    last_invoice = WholesaleInventory.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'BAKINVEN0001'

    invoice_id = last_invoice.inventory_id
    invoice_int = int(invoice_id.split('BAKINVEN000')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'BAKINVEN000'  + str(new_invoice_int)
    return new_invoice_id


class WholesaleInventory(models.Model):
    created = models.DateField(default=now, verbose_name = "Date")
    inventory_id = models.CharField(max_length = 500,default=increment_inventory_number, null = True, blank = True, verbose_name="Inventory Id")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    department_name =  models.ForeignKey(Department, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Department')

    def __str__(self):
        return str(self.inventory_id)

    class Meta():
        verbose_name = 'Wholesale Inventory'
        verbose_name_plural = 'Wholesale Inventory'


class WholesaleInventoryItems(models.Model):
    Status = (
        ('Opening Stock', 'Opening Stock'),
        ('Closing Stock', 'Closing Stock'),
    )
    created = models.DateField(default=now, verbose_name = "Date")
    inventory_id = models.ForeignKey(WholesaleInventory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Invoice Id")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    status =  models.CharField(max_length = 500, choices=Status,  default='Morning', null = True, blank = True )
    raw_material_name = models.ForeignKey(RawMaterials, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True,)

    class Meta():
        verbose_name = 'Wholesale Inventory Item'
        verbose_name_plural = 'Wholesale Inventory Items'

    # Overriding the save method to update invoice total for each new item
    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        #self.total_amount = order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
        #self.invoice.save()
        super().save(*args, **kwargs)


#---------------------- Invoice Number for Invoice Model-------------------#
#--------------------------------------------------------------------------#
###########   #############   #############   #############   #############
#---------------------------- Wholesale Inventory -------------------------#
#############   #############   #############   #############   ###########

def increment_production_number():
    last_invoice = WholesaleProduction.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'BAKPROD0001'

    invoice_id = last_invoice.production_id
    invoice_int = int(invoice_id.split('BAKPROD000')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'BAKPROD000'  + str(new_invoice_int)
    return new_invoice_id


class WholesaleProduction(models.Model):
    DEPARTMENTS = (
        ('Wholesale', 'Wholesale'),
    )




    SESSIONS = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    )


    created_at = models.DateField("Date", default=now)
    production_id = models.CharField(max_length = 500,default=increment_production_number, null = True, blank = True)
    department =  models.CharField(max_length = 500, choices=DEPARTMENTS, default='Wholesale', null = True, blank = True, verbose_name = 'Department')
    sub_department =  models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Sub Department')
    session = models.CharField(max_length = 500, choices=SESSIONS, default='', null = True, blank = True, verbose_name = 'Session')
    supervisor =  models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name = 'Supervisor')


    def __str__(self):
        return self.production_id


    class Meta():
                verbose_name = 'Wholesale Production'
                verbose_name_plural = 'Wholesale Production'


class WholesaleRawMaterialUsage(models.Model):

    DIRECT_INDIRECT = (
        ('Direct', 'Direct'),
        ('Indirect', 'Indirect'),
    )


    SESSIONS = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    )

    MIXTURES = (
        ('First Mixture', 'First Mixture'),
        ('Second Mixture', 'Second Mixture'),
        ('Third Mixture', 'Third Mixture'),
        ('Fourth Mixture', 'Fourth Mixture'),
        ('Fifth Mixture', 'Fifth Mixture'),
        ('Sixth Mixture', 'Sixth Mixture'),
        ('Seventh Mixture', 'Seventh Mixture'),
        ('Eighth Mixture', 'Eighth Mixture'),
        ('Ninth Mixture', 'Ninth Mixture'),
        ('Tenth Mixture', 'Tenth Mixture'),
        ('Eleventh Mixture', 'Eleventh Mixture'),
        ('Twelfth Mixture', 'Twelfth Mixture'),
        ('Thirteenth Mixture', 'Thirteenth Mixture'),
        ('Fourteenth Mixture', 'Fourteenth Mixture'),
        ('Fifteenth Mixture', 'Fifteenth Mixture'),
        ('Sixteenth Mixture', 'Sixteenth Mixture'),
        ('Seventeenth Mixture', 'Seventeenth Mixture'),
        ('Eighteenth Mixture', 'Eighteenth Mixture'),
        ('Ninteenth Mixture', 'Nineteenth Mixture'),
        ('Twentieth Mixture', 'Twentieth Mixture'),
        ('Twenty First Mixture', 'Twenty First Mixture'),
        ('Twenty Second Mixture', 'Twenty Second Mixture'),
        ('Twenty Third Mixture', 'Twenty Third Mixture'),
    )
  

    production_id = models.ForeignKey(WholesaleProduction, null=True, on_delete=models.SET_NULL)
    mixture_number =  models.CharField(max_length = 500, choices=MIXTURES, default='', null = True, blank = True, verbose_name = 'Mixture Number')
    raw_material = models.ForeignKey(RawMaterials, null=True, on_delete=models.SET_NULL, verbose_name = 'Raw Material')
    qty = models.DecimalField(max_digits=20, decimal_places=2, null = True, blank = True, default=0, verbose_name="Quantity Used")
    rm_total_weight_grams = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'RM Total Weight (Grams)')
    unit_cost_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True,  verbose_name = 'Unit Cost Price')
    raw_material_value = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Raw Material Value')


    class Meta():
        verbose_name = 'Wholesale Raw Material Usage'
        verbose_name_plural = 'Wholesale Raw Material Usage'

    @property
    def get_total_weight(self):
        virtual_amount = 0

        if self.production_id:
            if self.raw_material.entry_measure == "Grams":
                return self.qty
            else:
                return self.raw_material.weight_pack * self.qty
        else:
            return virtual_amount

    @property
    def get_weight_pack(self):
        return self.raw_material.weight_pack


    def save(self, *args, **kwargs):
        self.rm_total_weight_grams  = self.get_total_weight
        self.raw_material_value   = self.qty * self.unit_cost_price
        super().save(*args, **kwargs)


class WholesaleProductionOutput(models.Model):
    MIXTURES = (
        ('First Mixture', 'First Mixture'),
        ('Second Mixture', 'Second Mixture'),
        ('Third Mixture', 'Third Mixture'),
        ('Fourth Mixture', 'Fourth Mixture'),
        ('Fifth Mixture', 'Fifth Mixture'),
        ('Sixth Mixture', 'Sixth Mixture'),
        ('Seventh Mixture', 'Seventh Mixture'),
        ('Eighth Mixture', 'Eighth Mixture'),
        ('Ninth Mixture', 'Ninth Mixture'),
        ('Tenth Mixture', 'Tenth Mixture'),
        ('Eleventh Mixture', 'Eleventh Mixture'),
        ('Twelfth Mixture', 'Twelfth Mixture'),
        ('Thirteenth Mixture', 'Thirteenth Mixture'),
        ('Fourteenth Mixture', 'Fourteenth Mixture'),
        ('Fifteenth Mixture', 'Fifteenth Mixture'),
        ('Sixteenth Mixture', 'Sixteenth Mixture'),
        ('Seventeenth Mixture', 'Seventeenth Mixture'),
        ('Eighteenth Mixture', 'Eighteenth Mixture'),
        ('Ninteenth Mixture', 'Nineteenth Mixture'),
        ('Twentieth Mixture', 'Twentieth Mixture'),
        ('Twenty First Mixture', 'Twenty First Mixture'),
        ('Twenty Second Mixture', 'Twenty Second Mixture'),
        ('Twenty Third Mixture', 'Twenty Third Mixture'),

    )

    OUTPUTCATEGORY = (
        ('Finished', 'Finished'),
        ('SemiFinished', 'SemiFinished'),
    )

    TAG = (
        ('Opening Stock', 'Opening Stock'),
        ('Production', 'Production'),
        ('Closing Stock', 'Closing Stock'),
    )

    production_id = models.ForeignKey(WholesaleProduction, null=True, on_delete=models.SET_NULL)
    output_category =  models.CharField(max_length = 500, choices=OUTPUTCATEGORY, default='Finished', null = True, blank = True, verbose_name = 'Output Category')
    mixture_number =  models.CharField(max_length = 500, choices=MIXTURES, default='', null = True, blank = True, verbose_name = 'Mixture Number')
    tag =  models.CharField(max_length=200, choices=TAG, default='', verbose_name = 'Product Tag')
    product = models.ForeignKey(WholesaleProduct, null=True, on_delete=models.SET_NULL)
    qty = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Quantity')
    product_price = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Price')
    value = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Output Value')


    class Meta():
        verbose_name = 'Wholesale Production Output'
        verbose_name_plural = 'Wholesale Production Output'


    @property
    def get_weight_pack(self):
        return self.raw_material.weight_pack

    def save(self, *args, **kwargs):
        self.value   = self.qty * self.product_price
        super().save(*args, **kwargs)

class WholesaleConsumptionDamages(models.Model):
    STATUS = (
        ('Consumption', 'Consumption'),
        ('Damages', 'Damages'),
    )
    SESSIONS = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    )
    SUBDEPARTMENTS = (
        ('Boulangerie Morning', 'Boulangerie Morning'),
        ('Boulangerie Evening', 'Boulangerie Evening'),
        ('Patisserie Morning', 'Patisserie Morning'),
        ('Patisserie Evening', 'Patisserie Evening'),
        ('All', 'All'),

    )

    production_id = models.ForeignKey(WholesaleProduction, null = True, blank = True, on_delete=models.SET_NULL)
    status =  models.CharField(max_length = 500, choices=STATUS, default='', null = True, blank = True, verbose_name = 'Status')
    sub_department =  models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Sub Department')
    session = models.CharField(max_length = 500, choices=SESSIONS, default='', null = True, blank = True, verbose_name = 'Session')
    employee = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name = 'Employee')
    product = models.ForeignKey(WholesaleProduct, null=True, on_delete=models.SET_NULL)
    qty = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Quantity')
    product_price = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Price')
    value = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Output Value')


    class Meta():
        verbose_name = 'Wholesale Consumption & Damages'
        verbose_name_plural = 'Wholesale Consumption & Damages'

    #@property
    #def get_weight_pack(self):
        #return self.raw_material.weight_pack


    def save(self, *args, **kwargs):
        self.value   = self.qty * self.product_price
        super().save(*args, **kwargs)
'''