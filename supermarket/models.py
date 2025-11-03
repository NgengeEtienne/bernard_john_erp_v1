from django.db import models
from django.template.defaultfilters import slugify
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
import os




#############   #############   #############   #############   #############
#------------------------- Product / Category ------------------------------#
#############   #############   #############   #############   #############


class SupermarketProductCategory(models.Model):
    category_name = models.CharField(max_length=100, default='', verbose_name = "Category Name")
    sub_department = models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, null=True, blank =True, verbose_name = "Sub Department")


    def __str__(self):
        return str(self.category_name)

    class Meta:
        verbose_name = 'Supermarket Product Category'
        verbose_name_plural = 'Supermarket Product Category'

class SupermarketProductSubCategory(models.Model):
    sub_category_name = models.CharField(max_length=100, default='', verbose_name = "Sub Category Name")
    #category_name = models.ForeignKey(SupermarketProductCategory, on_delete=models.SET_NULL, null=True, blank =True, verbose_name = "Category")


    def __str__(self):
        return str(self.sub_category_name)

    class Meta:
        verbose_name = 'Supermarket Product Sub Category'
        verbose_name_plural = 'Supermarket Product Sub Category'


class SupermarketProduct(models.Model):
    product_name = models.CharField(max_length=100, default='', unique=True, verbose_name = "Product Name")
    sub_category_name = models.ForeignKey(SupermarketProductSubCategory, on_delete=models.SET_NULL, default=1, null = True, blank = True, verbose_name = "Category")
    barcode= models.CharField(max_length=100, default="", null = True, blank = True, verbose_name = "Barcode",)
    cost_price = models.DecimalField(max_digits=20, decimal_places=2, null = True, blank = True, default=0, verbose_name = "Cost Price")
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True, verbose_name = "Selling Price")
    #slug = models.SlugField(max_length=100, unique=True, blank=True)


    def __str__(self):
        return str(self.product_name)

    class Meta:
        verbose_name = 'Supermarket Product'
        verbose_name_plural = 'Supermarket Products'


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

class SupermarketCustomer(models.Model):
    def upload_to(instance, filename):
        ext = filename.split('.')[-1]
        new_filename = f"{uuid.uuid4()}.{ext}"
        return os.path.join('customer_photos', new_filename)

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
    customer_name = models.CharField(max_length=200,  unique=True,  verbose_name = "Customer Name")
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

   #'''Contact photo fields'''
    account_photo = models.ImageField(upload_to=upload_to, default='/static/app-assets/images/portrait/small/avatar-s-19.png',max_length=255)

    class Meta:
        verbose_name = 'Supermarket Customer'
        verbose_name_plural = 'Supermarket Customers'

    def __str__(self):
        return "{}".format(self.customer_name)


    def get_absolute_url(self):
        return reverse('customer:customer-details', args=[self.slug])

    def save(self, *args, **kwargs):
            self.slug = slugify(self.customer_name)
            super(SupermarketCustomer, self).save(*args, **kwargs)

    #class Meta:
        #ordering = ['-created']



#############   #############   #############   #############   #############
    #------------------------- Invoicing --------------------------------#
#############   #############   #############   #############   #############

def supermarket_increment_invoice_number():
    last_invoice = SupermarketInvoice.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'SUPINV0001'

    invoice_id = last_invoice.invoice_id
    invoice_int = int(invoice_id.split('SUPINV000')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'SUPINV000'  + str(new_invoice_int)
    return new_invoice_id

#############   #############   #############   #############   #############
    #------------------------- Invoicing --------------------------------#
#############   #############   #############   #############   #############

class SupermarketInvoice(models.Model):
    Sales_Session = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
        ('Wholeday', 'Wholeday'),
    )
    sales_person = (
        ('Moses', 'Moses'),
        ('Nelson', 'Nelson'),
    )
    Statustag = (
        ('Sales', 'Sales'),
        ('Return Inwards', 'Return Inwards'),
    ) 
    created = models.DateField(default=now, verbose_name = "Date")
    department_name =  models.ForeignKey(Department, on_delete=models.SET_NULL, default='Supermarket', null = True, blank = True, verbose_name = 'Department')
    invoice_id = models.CharField(max_length = 500, default=supermarket_increment_invoice_number, null = True, blank = True, verbose_name="Invoice Id")
    customer = models.ForeignKey(SupermarketCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    sales_session =  models.CharField(max_length = 500, choices=Sales_Session,  default='Morning', null = True, blank = True)
    due_date = models.DateField(null=True, blank=True, verbose_name = "Due Date")

    sales_person =  models.CharField(max_length=200, default='',choices=sales_person, verbose_name = "Sale Person")
    invoice_total = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Invoice Total")
    vat_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True,)
    apply_vat = models.BooleanField(default=False)
    status =  models.CharField(max_length = 500, choices=Statustag, null = True, blank = True)

    def __str__(self):
        return str(self.invoice_id)

    @property
    def total_amount(self):
        virtual_qty = 0
        if self.invoice_id:
            return sum([item.get_total_amount for item in self.supermarketinvoicedetail_set.all()])
        else:
            return virtual_qty

    @property
    def get_total_returns(self):
        virtual_qty = 0
        if self.invoice_id:
            return sum([item.total_return_amount for item in self.supermarketreturnsitems_set.all()])
        else:
            return virtual_qty
        
    @property
    def total_discount(self):
        if self.invoice_id:
            return sum([item.discount_value for item in self.supermarketinvoicedetail_set.all()])
        return Decimal(0)

    @property
    def get_grand_total(self):
        virtual_qty = 0
        if self.invoice_id:
            return sum([item.get_total_amount for item in self.supermarketinvoicedetail_set.all()]) + self.vat_amount - self.get_total_returns
        else:
            return virtual_qty

    @property
    def total_amount_paid(self):
        virtual_amount = 0
        if self.invoice_id:
            return sum([item.get_total_amount_paid for item in self.supermarketinvoicepayment_set.all()])
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

        return super(SupermarketInvoice, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Supermarket Customer Invoice'
        verbose_name_plural = 'Supermarket Customer Invoice'


class SupermarketInvoiceDetail(models.Model):
    invoice = models.ForeignKey(SupermarketInvoice, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Invoice Id")
    product = models.ForeignKey(SupermarketProduct, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    discount_price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    discount_value = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    net_amount = models.DecimalField(max_digits=20, decimal_places=0, default=0)

    @property
    def get_total_amount(self):
        total = (Decimal(self.quantity) * Decimal(self.price))
        return total
    
    def __str__(self):
        return str(self.net_amount)

    class Meta:
        verbose_name = 'Supermarket Customer InvoicedItems'
        verbose_name_plural = 'Supermarket Customer InvoicedItems'

# Overriding the save method to update invoice total for each new item
    def save(self, *args, **kwargs):
        self.total =(self.quantity) *(self.price)
        self.discount_value = (self.quantity) *(self.discount_price)
        self.net_amount = self.total - self.discount_value
        
        #self.total_amount = order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
        #self.invoice.save()
        super().save(*args, **kwargs)
        
#############   #############   #############   #############   #############
#------------------------- Supermarket Supplier ---------------------#
#############   #############   #############   #############   #############

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message='Phone number invalid. Should start with example: +237'
)

class SupermarketSupplier(models.Model):

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
        verbose_name = ' Supermarket Suppliers'
        verbose_name_plural = 'Supermarket Suppliers'

    def __str__(self):
        return "{}".format(self.supplier_name)


    def get_absolute_url(self):
        return reverse('supplier:supplier-details', args=[self.slug])

    def save(self, *args, **kwargs):
            self.slug = slugify(self.supplier_name)
            super(SupermarketSupplier, self).save(*args, **kwargs)

    #class Meta:
        #ordering = ['-created']

#----------------------------------Purchase Summary ---------------------------------------------#
#------------------------------------------------------------------------------------------------#
class SupermarketPurchaseSummary(models.Model):
    SubDepartment = (
        ('Boulangerie Morning', 'Boulangerie Morning'),
        ('Boulangerie Evening', 'Boulangerie Evening'),
        ('Patisserie', 'Patisserie'),
        ('Magazine', 'Magazine'),
    )
    created = models.DateField(default=now, verbose_name = "Date")
    purchase_id = models.CharField(max_length = 500,default='', null = True, blank = True, verbose_name="Purchase ID")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    supplier_name = models.ForeignKey(SupermarketSupplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Supplier's Name")
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

        return super(SupermarketPurchaseSummary, self).save(*args, **kwargs)


    class Meta():
        verbose_name = 'Supermarket Purchase Summary'
        verbose_name_plural = 'Supermarket Purchase Summary'
#----------------------------------Purchase Summary ---------------------------------------------#



    
#############   #############   #############   #############   #############
#---------------------------- Supermarket Raw Materials -------------------------#
#############   #############   #############   #############   #############
    
def increment_purchase_number():
    last_invoice = SupermarketPurchase.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'SUPPUR001'

    invoice_id = last_invoice.purchase_id
    invoice_int = int(invoice_id.split('SUPPUR00')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'SUPPUR00'  + str(new_invoice_int)
    return new_invoice_id


class SupermarketPurchase(models.Model):
    # SubDepartment = (
    #     ('Boulangerie Morning', 'Boulangerie Morning'),
    #     ('Boulangerie Evening', 'Boulangerie Evening'),
    #     ('Patisserie', 'Patisserie'),
    #     ('Magazine', 'Magazine'),
    # )
    def get_default_department():
        return Department.objects.get(pk=1)  # Replace with the correct default Department
    ordered_date = models.DateTimeField(default=now, verbose_name = "Ordered Date")
    recieved_date = models.DateTimeField(default=now, verbose_name = "Recieved Date")
    created = models.DateField(default=now, verbose_name = "Date")
    purchase_id = models.CharField(max_length = 500,default=increment_purchase_number, null = True, blank = True, verbose_name="Customer Name")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    supplier_name = models.ForeignKey(SupermarketSupplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Supplier's Name")
    department =  models.ForeignKey(Department, on_delete=models.SET_NULL, default=get_default_department, blank=True, null=True, verbose_name="Department")
    due_date = models.DateField(null=True, blank=True, verbose_name = "Due Date")
    purchase_total = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Purchase Total")
    vat_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="VAT Amount")
    discount_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Discount Amount")
    net_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Net Amount")
 

    def __str__(self):
        return str(self.purchase_id)
    
    def save(self, *args, **kwargs):
        if not self.id:
            year, month, day = map(int, self.created.split('-'))
            created_date = date(year, month, day)

            # Add 3 days
            due_date = created_date + timedelta(days=3)

            # Store due_date as a string again
            self.due_date = due_date.isoformat()
            self.net_amount = self.total_cost_price - Decimal(self.discount_value)

        return super(SupermarketPurchase, self).save(*args, **kwargs)

    class Meta():
        verbose_name = 'Supermarket Purchase Invoice'
        verbose_name_plural = 'Supermarket Purchase Invoice'



class SupermarketPurchaseItems(models.Model):
    def get_default_department():
        return Department.objects.get(pk=1)
    created = models.DateField(default=now, verbose_name = "Date")
    ordered_date = models.DateTimeField(default=now, verbose_name = "Ordered Date")
    recieved_date = models.DateTimeField(default=now, verbose_name = "Recieved Date")
    purchase_id = models.ForeignKey(SupermarketPurchase, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Purchase Id")
    product = models.ForeignKey(SupermarketProduct, related_name="raw_material_purchase", on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    unit_cost_price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    unit_selling_price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    total_cost_price = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True,)
    total_selling_price = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True,)
    discount_price = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Discount value")
    discount_value = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Discount Amount")
    net_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Net Amount")
    
    class Meta():
        verbose_name = 'Supermarket Purchase Item'
        verbose_name_plural = 'Supermarket Purchase Items'

    # Overriding the save method to update invoice total for each new item
    def save(self, *args, **kwargs):
        self.total_cost_price = Decimal(self.quantity) * Decimal(self.unit_cost_price)
        self.total_selling_price = Decimal(self.quantity) * Decimal(self.unit_selling_price)
        self.discount_value = Decimal(self.quantity) * Decimal(self.discount_price)
        self.net_amount = self.total_cost_price - Decimal(self.discount_value)
        
        #self.total_amount = order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
        #self.invoice.save()
        super().save(*args, **kwargs)
# #------------------------------------------------------------------------------------------------#
###########   #############   #############   #############   #############
#---------------------------- Supermarket Inventory -------------------------#
#############   #############   #############   #############   #############


        

#############   #############   #############   #############   #############
    #------------------------- Invoicing --------------------------------#
#############   #############   #############   #############   #############
def opening_bal_increment_invoice_number():
    last_invoice_payment = SupermarketCustomerOpeningBalance.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice_payment:
            return today_string + "-" + 'SUPCUSTOB0001'

    payment_id = last_invoice_payment.payment_id
    payment_int = int(payment_id.split('SUPCUSTOB000')[-1])
    new_payment_int = payment_int + 1

    new_payment_id = today_string + "-" + 'SUPCUSTOB000'  + str(new_payment_int)
    return new_payment_id

class SupermarketCustomerOpeningBalance(models.Model):
    Opening_bal_des = (
        ('Opening Balance', 'Opening Balance'),
    )

    date = models.DateField(default=now)
    invoice = models.ForeignKey(SupermarketInvoice, on_delete=models.SET_NULL, null = True, blank = True,)
    #opening_bal_id = models.CharField(max_length = 500,default=opening_bal_increment_invoice_number, null = True, blank = True, verbose_name = "Customer Name")
    customer = models.ForeignKey(SupermarketCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    description =  models.CharField(max_length = 500, choices=Opening_bal_des,  default='Customer Opening Balance', null = True, blank = True, verbose_name = "Description")
    amount_owed = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    

    def __str__(self):
        return self.opening_bal_id

    class Meta:
        verbose_name = 'Supermarket Customer Opening Balance'
        verbose_name_plural = 'Supermarket Customer Opening Balance'    
        
#-----------------------------------------------------------------------------#
#############   #############   #############   #############   #############
    #------------------------- Payments --------------------------------#
#############   #############   #############   #############   #############
def increment_invoice_number():
    last_invoice_payment = SupermarketInvoicePayment.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice_payment:
            return today_string + "-" + 'SMKPAYMT0001'

    payment_id = last_invoice_payment.payment_id
    payment_int = int(payment_id.split('SMKPAYMT000')[-1])
    new_payment_int = payment_int + 1

    new_payment_id = today_string + "-" + 'SMKPAYMT000'  + str(new_payment_int)
    return new_payment_id

class SupermarketInvoicePayment(models.Model):
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
    invoice = models.ForeignKey(SupermarketInvoice, on_delete=models.SET_NULL, null = True, blank = True,)
    payment_id = models.CharField(max_length = 500,default=increment_invoice_number, null = True, blank = True)
    customer = models.ForeignKey(SupermarketCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    payment_installment =  models.CharField(max_length = 500, choices=Payment_Installment,  default='1st Installment', null = True, blank = True)
    employee = models.CharField(max_length = 500, null = True, blank = True, default='')
    amount_paid = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    

    def __str__(self):
        return self.payment_installment

    @property
    def get_total_amount_paid(self):
        return self.amount_paid

    class Meta():
        verbose_name = 'Supermarket Customers Payments'
        verbose_name_plural = 'Supermarket Customers Payments'



#------------------------------------------------------------------------------------------------#
#----------------------------------- Supermarket Return Items ----------------------------------------#
#------------------------------------------------------------------------------------------------#
class SupermarketReturnsItems(models.Model):
    Sales_Session = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    )

    date = models.DateField(default=now)
    customer = models.ForeignKey(SupermarketCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    #sales_person =  models.CharField(max_length=200, default='', verbose_name = "Sale Person")
    invoice = models.ForeignKey(SupermarketInvoice, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Invoice Id")
    product = models.ForeignKey(SupermarketProduct, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
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
#------------------------- Supermarket Supplier ---------------------#
#############   #############   #############   #############   #############

                               
        
class SupermarketPurchasePayment(models.Model):
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
    invoice = models.ForeignKey(SupermarketInvoice, on_delete=models.SET_NULL, null = True, blank = True,)
    customer = models.ForeignKey(SupermarketCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    payment_installment =  models.CharField(max_length = 500, choices=Payment_Installment,  default='1st Installment', null = True, blank = True)
    employee = models.CharField(max_length = 500, null = True, blank = True, default='')
    amount_paid = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    payment_id = models.CharField(max_length = 500,default=increment_invoice_number, null = True, blank = True)

    def __str__(self):
        return self.payment_installment

    @property
    def get_total_amount_paid(self):
        return self.amount_paid

    class Meta():
        verbose_name = 'Supermarket Purchase Payments'
        verbose_name_plural = 'Supermarket Purchase Payments'

#------------------------------------------------------------------------------------------------#
###########   #############   #############   #############   #############
#---------------------------- Supermarket Inventory -------------------------#
#############   #############   #############   #############   #############

def increment_inventory_number():
    last_invoice = SupermarketInventory.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'SMKINVEN0001'

    invoice_id = last_invoice.inventory_id
    invoice_int = int(invoice_id.split('SMKINVEN000')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'SMKINVEN000'  + str(new_invoice_int)
    return new_invoice_id


class SupermarketInventory(models.Model):
    created = models.DateField(default=now, verbose_name = "Date")
    inventory_id = models.CharField(max_length = 500,default=increment_inventory_number, null = True, blank = True, verbose_name="Inventory Id")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    department_name =  models.ForeignKey(Department, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Department')

    def __str__(self):
        return str(self.inventory_id)

    class Meta():
        verbose_name = 'Supermarket Inventory'
        verbose_name_plural = 'Supermarket Inventory'


class SupermarketInventoryItems(models.Model):
    Status = (
        ('Opening Stock', 'Opening Stock'),
        ('Closing Stock', 'Closing Stock'),
    )
    created = models.DateField(default=now, verbose_name = "Date")
    inventory_id = models.ForeignKey(SupermarketInventory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Invoice Id")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    status =  models.CharField(max_length = 500, choices=Status,  default='Morning', null = True, blank = True )
    raw_material_name = models.ForeignKey(SupermarketProduct, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True,)

    class Meta():
        verbose_name = 'Supermarket Inventory Item'
        verbose_name_plural = 'Supermarket Inventory Items'

    # Overriding the save method to update invoice total for each new item
    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        #self.total_amount = order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
        #self.invoice.save()
        super().save(*args, **kwargs)


#---------------------- Invoice Number for Invoice Model-------------------#
#--------------------------------------------------------------------------#
###########   #############   #############   #############   #############
#---------------------------- Supermarket Inventory -------------------------#
#############   #############   #############   #############   ###########

def increment_production_number():
    last_invoice = SupermarketProduction.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'SMKPROD0001'

    invoice_id = last_invoice.production_id
    invoice_int = int(invoice_id.split('SMKPROD000')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'SMKPROD000'  + str(new_invoice_int)
    return new_invoice_id


class SupermarketProduction(models.Model):
    DEPARTMENTS = (
        ('Supermarket', 'Supermarket'),
    )




    SESSIONS = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    )


    created_at = models.DateField("Date", default=now)
    production_id = models.CharField(max_length = 500,default=increment_production_number, null = True, blank = True)
    department =  models.CharField(max_length = 500, choices=DEPARTMENTS, default='Supermarket', null = True, blank = True, verbose_name = 'Department')
    sub_department =  models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Sub Department')
    session = models.CharField(max_length = 500, choices=SESSIONS, default='', null = True, blank = True, verbose_name = 'Session')
    supervisor =  models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name = 'Supervisor')


    def __str__(self):
        return self.production_id


    class Meta():
                verbose_name = 'Supermarket Production'
                verbose_name_plural = 'Supermarket Production'


class SupermarketConsumptionDamages(models.Model):
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

    production_id = models.ForeignKey(SupermarketProduction, null = True, blank = True, on_delete=models.SET_NULL)
    status =  models.CharField(max_length = 500, choices=STATUS, default='', null = True, blank = True, verbose_name = 'Status')
    sub_department =  models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Sub Department')
    session = models.CharField(max_length = 500, choices=SESSIONS, default='', null = True, blank = True, verbose_name = 'Session')
    employee = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name = 'Employee')
    product = models.ForeignKey(SupermarketProduct, null=True, on_delete=models.SET_NULL)
    qty = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Quantity')
    product_price = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Price')
    value = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Output Value')


    class Meta():
        verbose_name = 'Supermarket Consumption & Damages'
        verbose_name_plural = 'Supermarket Consumption & Damages'

    #@property
    #def get_weight_pack(self):
        #return self.raw_material.weight_pack


    def save(self, *args, **kwargs):
        self.value   = self.qty * self.product_price
        super().save(*args, **kwargs)
