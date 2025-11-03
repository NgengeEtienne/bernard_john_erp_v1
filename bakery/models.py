from django.db import models
from django.template.defaultfilters import slugify
from django.utils.text import slugify
from django.db import IntegrityError
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
from django.db.models.signals import post_save
import os
import uuid
from django.db.models import Avg, StdDev
import math
import re
from datetime import date, datetime


#############   #############   #############   #############   #############
#---------------------------- Bakery Raw Materials -------------------------#
#############   #############   #############   #############   #############


#====================== Raw Material Category ==================================#
class RawMaterialCategory(models.Model):
    raw_material_category_name = models.CharField(max_length=100, default='', verbose_name = "Category Name")

    def __str__(self):
        return str(self.raw_material_category_name)

    class Meta:
        verbose_name = 'Raw Material Categories'
        verbose_name_plural = 'Raw Material Categories'

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
    
    Perishable_non_Perishable = (
        ('Perishable', 'Perishable'),
        ('Non Perishable', 'Non Perishable'),
    )

    raw_material_name =  models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name = 'Raw Material')
    raw_material_category =models.ForeignKey(RawMaterialCategory, default="", on_delete=models.SET_NULL, null=True, blank =True, verbose_name = "Raw Material Category")
    category=  models.CharField(max_length = 500, choices=CATEGORY, default='Direct', null = True, blank = True, verbose_name = 'Category')
    perish_non_perish=  models.CharField(max_length = 500, choices=Perishable_non_Perishable, default='Perishable', null = True, blank = True, verbose_name = 'Perishable / Non Perishable')
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
#------------------------- Product / Category ------------------------------#
#############   #############   #############   #############   #############

#====================== Product Category ==================================#
class BakeryProductCategory(models.Model):
    category_name = models.CharField(max_length=100, default='', verbose_name = "Category Name")
    sub_department = models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, null=True, blank =True, verbose_name = "Sub Department")


    def __str__(self):
        return str(self.category_name)

    class Meta:
        verbose_name = 'Bakery Product Category'
        verbose_name_plural = 'Bakery Product Category'

#=================================== Recipe ==================================#
class Recipe(models.Model):
    recipe_name = models.CharField(max_length=255, null=True, blank =True, verbose_name = "Recipe Name")

    def __str__(self):
        return self.recipe_name

#=================================== Production ==================================#
class BakeryProduct(models.Model):
    product_name = models.CharField(max_length=100, default='', unique=True, verbose_name = "Product Name")
    category = models.ForeignKey(BakeryProductCategory, on_delete=models.SET_NULL, default=1, null = True, blank = True, verbose_name = "Category")
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name = "Supply Price")
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True, verbose_name = "Selling Price")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    entry_weight_per_boule = models.CharField(max_length=100, default=0, null = True, blank = True, verbose_name = "Entry Weight/Boule")
    weight_per_boule_kg = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True, verbose_name = "Weight/Boule/kg")
    weight_per_boule_gram = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True, verbose_name = "Weight/Boule/grams")
    output_per_boule = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True, verbose_name = "Output/Boule")
    unit_output_weight = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True, verbose_name = "Weight/Unit Output/grams")
    
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, default="", null = True, blank = True, verbose_name = "Recipe") 

    def __str__(self):
        return str(self.product_name)

    def get_absolute_url(self):
        return reverse('bakery:product-details', args=[self.slug])

    def save(self, *args, **kwargs):
            self.slug = slugify(self.product_name)
            super(BakeryProduct, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'Bakery Product'
        verbose_name_plural = 'Bakery Products'

#=================================== Product Recipe ==================================#
class ProductRecipe(models.Model):
    product = models.ForeignKey(BakeryProduct, on_delete=models.SET_NULL, default=1, null = True, blank = True, verbose_name = "Product Name")
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, default=1, null = True, blank = True, verbose_name = "Recipe")
    quantity_per_product = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity of recipe per product")

    #def __str__(self):
        #return f"{self.product}"
    class Meta:
        verbose_name = 'Product Recipe'
        verbose_name_plural = 'Product Recipes'

#=================================== Product Recipe ==================================#
class RecipeRawMaterial(models.Model):
    
    
    ENTRYMEASURE = (
        ('Grams', 'Grams'),
        ('Kg', 'Kg'),
        ('Unit', 'Unit'),
        ('Litre', 'Litre'),
        ('Ml', 'Ml'),

    )
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, default=1, null = True, blank = True, verbose_name = "Recipe")
    raw_material = models.ForeignKey(RawMaterials, on_delete=models.SET_NULL, default=1, null = True, blank = True, verbose_name = "Raw Material")
    quantity_per_recipe = models.DecimalField(max_digits=100, decimal_places=8, help_text="Quantity of raw material per recipe unit")
    measure =  models.CharField(max_length=200, default="", choices=ENTRYMEASURE, verbose_name = 'Entry Measure')
    #def __str__(self):
        #return f"{self.recipe}"
 
#############   #############   #############   #############   #############
    #------------------------- Customer --------------------------------#
#############   #############   #############   #############   #############


# Create your models here.
#---------------------- Invoice Number for Invoice Model----------------------#

# Create your models here.

   
    


# phone validator using regular expressions
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message='Phone number invalid. Should start with example: +237'
)

class BakeryCustomer(models.Model):
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
    '''General information fields'''
    
    customer_name = models.CharField(max_length=200,  verbose_name = "Customer Name")
    customer_type = models.CharField(max_length=100, choices=Customer_TYPE , null = True, blank = True, verbose_name = "Customer Type")
    company_name = models.CharField(max_length=200, default='', null = True, blank = True, verbose_name = "Company Name")
    company_box = models.CharField(max_length=100, choices=Company_box, null = True, blank = True, verbose_name = "Own Company Box")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    '''Contact details fields'''
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

    '''Contact photo fields'''
    account_photo = models.ImageField(upload_to=upload_to, default='/static/app-assets/images/portrait/small/avatar-s-19.png',max_length=255)

    class Meta:
        verbose_name = 'Bakery Customer'
        verbose_name_plural = 'Bakery Customers'

    def __str__(self):
        return "{}".format(self.customer_name)


    def get_absolute_url(self):
        return reverse('customer:customer-details', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.customer_name)
            slug = original_slug
            counter = 1
            while BakeryCustomer.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            self.slug = slug
        super(BakeryCustomer, self).save(*args, **kwargs)

#############   #############   #############   #############   #############
    #------------------------- Invoicing --------------------------------#
#############   #############   #############   #############   #############

def bakery_increment_invoice_number():
    last_invoice = BakeryInvoice.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'BAKINV0001'

    invoice_id = last_invoice.invoice_id
    invoice_int = int(invoice_id.split('BAKINV000')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'BAKINV000'  + str(new_invoice_int)
    return new_invoice_id

#############   #############   #############   #############   #############
    #------------------------- Invoicing --------------------------------#
#############   #############   #############   #############   #############

class BakeryInvoice(models.Model):
    Sales_Session = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    )
    sales_person = (
        ('Moses', 'Moses'),
        ('Nelson', 'Nelson'),
    ) 
    Statustag = (
        ('Sales', 'Sales'),
        ('Return Inwards', 'Return Inwards'),
    ) 
    sales_person =  models.CharField(max_length=200, default='', choices= sales_person, verbose_name = "Sale Person")
    created = models.DateField(default=now, verbose_name = "Date")
    invoice_id = models.CharField(max_length = 500, default=bakery_increment_invoice_number, null = True, blank = True, verbose_name="Invoice Id")
    customer = models.ForeignKey(BakeryCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    sales_session =  models.CharField(max_length = 400, choices=Sales_Session,  default='Morning', null = True, blank = True)
    due_date = models.DateField(null=True, blank=True, verbose_name = "Due Date")
    invoice_total = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Invoice Total")
    vat_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True,)
    apply_vat = models.BooleanField(default=False)
    status =  models.CharField(max_length = 500, choices=Statustag,  default='Sales', null = True, blank = True)

    def __str__(self):
        return str(self.invoice_id)

    @property
    def total_amount(self):
        virtual_qty = 0
        if self.invoice_id:
            return sum([item.get_total_amount for item in self.bakeryinvoicedetail_set.all()])
        else:
            return virtual_qty

    @property
    def total_amount(self):
        virtual_qty = 0
        if self.invoice_id:
            return sum([item.get_total_amount for item in self.bakeryinvoicedetail_set.all()])
        else:
            return virtual_qty
    @property
    def get_total_returns(self):
        virtual_qty = 0
        if self.invoice_id:
            return sum([item.total_return_amount for item in self.bakeryreturnsitems_set.all()])
        else:
            return virtual_qty
    @property
    def get_discount_total(self):
        virtual_qty = 0
        if self.invoice_id:
            return sum([item.get_discount_value for item in self.bakeryinvoicedetail_set.all()])
        else:
            return virtual_qty
    @property
    def get_discount_percentage(self):
        # Default value when invoice_id is not set
        virtual_qty = Decimal('0.00')

        if self.invoice_id:
            # Ensure total_amount is not zero to avoid division by zero
            if self.total_amount == 0:
                return virtual_qty
            return (self.get_discount_total / self.total_amount) * 100
        else:
            return virtual_qty
    @property
    def get_grand_total(self):
        virtual_qty = 0
        if self.invoice_id:
            return sum([item.get_total_amount for item in self.bakeryinvoicedetail_set.all()]) + self.vat_amount - self.get_total_returns - self.get_discount_total
        else:
            return virtual_qty
    @property
    def total_amount_paid(self):
        virtual_amount = 0
        if self.invoice_id:
            return sum([item.get_total_amount_paid for item in self.bakeryinvoicepayment_set.all()])
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
        if not self.invoice_id:  # Only generate if it hasn't been set
            self.invoice_id = bakery_increment_invoice_number(self)
            
        if not self.id:
            #self.due_date = datetime.datetime.now()+ datetime.timedelta(days=3)
            year, month, day = map(int, self.created.split('-'))
            created_date = date(year, month, day)

            # Add 3 days
            due_date = created_date + timedelta(days=3)

            # Store due_date as a string again
            self.due_date = due_date.isoformat() 

        return super(BakeryInvoice, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Bakery Customer Invoice'
        verbose_name_plural = 'Bakery Customer Invoice'
    

class BakeryInvoiceDetail(models.Model):
    invoice = models.ForeignKey(BakeryInvoice, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Invoice Id")
    product = models.ForeignKey(BakeryProduct, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
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
    
    @property
    def get_discount_value(self):
        total = (Decimal(self.quantity) * Decimal(self.discount_price))
        return total
    
    @property
    def get_discount_percentage(self):
        total = (Decimal(self.discount_price) / Decimal(self.price)) *100
        return total
    
    @property
    def get_net_amount(self):
        total = (Decimal(self.total) - Decimal(self.discount_value))
        return total

    class Meta:
        verbose_name = 'Bakery Customer InvoicedItems'
        verbose_name_plural = 'Bakery Customer InvoicedItems'

# Overriding the save method to update invoice total for each new item
    def save(self, *args, **kwargs):
        self.total =(self.quantity) *(self.price)
        self.discount_value = (self.quantity) *(self.discount_price)
        self.net_amount = self.total - self.discount_value
        
        #self.total_amount = order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
        #self.invoice.save()
        super().save(*args, **kwargs)
        


#############   #############   #############   #############   #############
    #------------------------- Invoicing --------------------------------#
#############   #############   #############   #############   #############
def opening_bal_increment_invoice_number():
    last_invoice_payment = BakeryCustomerOpeningBalance.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice_payment:
            return today_string + "-" + 'BAKCUSTOB0001'

    payment_id = last_invoice_payment.payment_id
    payment_int = int(payment_id.split('BAKCUSTOB000')[-1])
    new_payment_int = payment_int + 1

    new_payment_id = today_string + "-" + 'BAKCUSTOB000'  + str(new_payment_int)
    return new_payment_id

class BakeryCustomerOpeningBalance(models.Model):
    Opening_bal_des = (
        ('Opening Balance', 'Opening Balance'),
    )

    date = models.DateField(default=now)
    invoice = models.ForeignKey(BakeryInvoice, on_delete=models.SET_NULL, null = True, blank = True,)
    opening_bal_id = models.CharField(max_length = 500,default=opening_bal_increment_invoice_number, null = True, blank = True, verbose_name = "Customer Name")
    customer = models.ForeignKey(BakeryCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    description =  models.CharField(max_length = 500, choices=Opening_bal_des,  default='Customer Opening Balance', null = True, blank = True, verbose_name = "Description")
    amount_owed = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    

    def __str__(self):
        return self.opening_bal_id

    class Meta:
        verbose_name = 'Bakery Customer Opening Balance'
        verbose_name_plural = 'Bakery Customer Opening Balance'    
        
#-----------------------------------------------------------------------------#
#############   #############   #############   #############   #############
    #------------------------- Payments --------------------------------#
#############   #############   #############   #############   #############
def increment_invoice_number():
    last_invoice_payment = BakeryInvoicePayment.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice_payment:
            return today_string + "-" + 'BAKPAYMT0001'

    payment_id = last_invoice_payment.payment_id
    payment_int = int(payment_id.split('BAKPAYMT000')[-1])
    new_payment_int = payment_int + 1

    new_payment_id = today_string + "-" + 'BAKPAYMT000'  + str(new_payment_int)
    return new_payment_id

class BakeryInvoicePayment(models.Model):
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
    invoice = models.ForeignKey(BakeryInvoice, on_delete=models.SET_NULL, null = True, blank = True,)
    payment_id = models.CharField(max_length = 500,default=increment_invoice_number, null = True, blank = True)
    customer = models.ForeignKey(BakeryCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    payment_installment =  models.CharField(max_length = 500, choices=Payment_Installment,  default='1st Installment', null = True, blank = True)
    employee = models.CharField(max_length = 500, null = True, blank = True, default='')
    amount_paid = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    

    def __str__(self):
        return self.payment_installment

    @property
    def get_total_amount_paid(self):
        return self.amount_paid

    class Meta():
        verbose_name = 'Bakery Customers Payments'
        verbose_name_plural = 'Bakery Customers Payments'



#------------------------------------------------------------------------------------------------#
#----------------------------------- Bakery Return Items ----------------------------------------#
#------------------------------------------------------------------------------------------------#
class BakeryReturnsItems(models.Model):
    Sales_Session = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    )

    date = models.DateField(default=now)
    customer = models.ForeignKey(BakeryCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    #sales_person =  models.CharField(max_length=200, default='', verbose_name = "Sale Person")
    invoice = models.ForeignKey(BakeryInvoice, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Invoice Id")
    product = models.ForeignKey(BakeryProduct, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
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
#------------------------- Bakery Supplier ---------------------#
#############   #############   #############   #############   #############

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message='Phone number invalid. Should start with example: +237'
)

class BakerySupplier(models.Model):

    Supplier_TYPE = (

        ('Company', 'Company'),
        ('Enterprise', 'Enterprise'),
        ('Individual', 'Individual'),

    )

    '''General information fields'''
    supplier_name = models.CharField(max_length=200,  verbose_name = "Supplier Name")
    supplier_type = models.CharField(max_length=100, choices=Supplier_TYPE , null = True, blank = True, verbose_name = "Supplier Type")
    company_name = models.CharField(max_length=200, default='', null = True, blank = True, verbose_name = "Company Name")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    '''Contact details fields'''
    address = models.TextField(max_length=2550, null = True, blank = True, verbose_name = "Address")
    city = models.CharField(max_length=100, default='Kumba', null = True, blank = True, verbose_name = "City")
    region = models.CharField(max_length=200, default='South West Region', null = True, blank = True, verbose_name = "Region")
    phone1 = models.CharField(validators=[phone_regex], max_length=15, null=True, blank = True, verbose_name = "Phone 1 +237")
    phone2 = models.CharField(validators=[phone_regex], max_length=15, null=True, blank = True, verbose_name = "Phone 2 +237")
    email = models.EmailField(blank=True, null=True, verbose_name = "Email")

    class Meta:
        verbose_name = ' Bakery Suppliers'
        verbose_name_plural = 'Bakery Suppliers'

    def __str__(self):
        return "{}".format(self.supplier_name)


    def get_absolute_url(self):
        return reverse('supplier:supplier-details', args=[self.slug])

    def save(self, *args, **kwargs):
            self.slug = slugify(self.supplier_name)
            super(BakerySupplier, self).save(*args, **kwargs)

    #class Meta:
        #ordering = ['-created']

#----------------------------------Purchase Summary ---------------------------------------------#
#------------------------------------------------------------------------------------------------#
class BakeryPurchaseSummary(models.Model):
    SubDepartment = (
        ('Boulangerie Morning', 'Boulangerie Morning'),
        ('Boulangerie Evening', 'Boulangerie Evening'),
        ('Patisserie', 'Patisserie'),
        ('Magazine', 'Magazine'),
    )
    created = models.DateField(default=now, verbose_name = "Date")
    purchase_id = models.CharField(max_length = 500,default='', null = True, blank = True, verbose_name="Purchase ID")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    supplier_name = models.ForeignKey(BakerySupplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Supplier's Name")
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

        return super(BakeryPurchaseSummary, self).save(*args, **kwargs)


    class Meta():
        verbose_name = 'Bakery Purchase Summary'
        verbose_name_plural = 'Bakery Purchase Summary'
#----------------------------------Purchase Summary ---------------------------------------------#



    
#############   #############   #############   #############   #############
#---------------------------- Bakery Raw Materials Purchase-------------------------#
#############   #############   #############   #############   #############
    


def increment_purchase_number():
    last_invoice = BakeryPurchase.objects.all().order_by('id').last()
    today = date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
        return today_string + "-" + 'BAKPUR001'

    invoice_id = last_invoice.purchase_id
    match = re.match(r'(\d{4}-\d{1,2}-\d{1,2})-(INV|BAKPUR)(\d+)', invoice_id)
    if match:
        date_string, prefix, number = match.groups()
        invoice_int = int(number)
        new_invoice_int = invoice_int + 1
        new_invoice_id = today_string + "-" + prefix + str(new_invoice_int).zfill(4)
        return new_invoice_id
    else:
        raise ValueError("Unexpected format for invoice_id: " + invoice_id)



class BakeryPurchase(models.Model):  
    created = models.DateField(default=now, verbose_name = "Date")
    department =models.CharField(max_length = 100,  default='Bakery', null = True, blank = True,verbose_name="Department")
    ordered_date = models.DateTimeField( blank=False, null=False, verbose_name="Order Data-Time")
    recieved_date = models.DateTimeField( blank=False, null=False, verbose_name="Received Date-Time")
    
    purchase_id = models.CharField(max_length = 500,default=increment_purchase_number, null = True, blank = True, verbose_name="Customer Name")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    supplier_name = models.ForeignKey(BakerySupplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Supplier's Name")
    due_date = models.DateField(null=True, blank=True, verbose_name = "Due Date")
    purchase_total = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Purchase Total")
    
    def __str__(self):
        return str(self.purchase_id)
    
    def save(self, *args, **kwargs):
        if not self.id:  # Only set the due date on creation
            if not self.due_date:  # Calculate the due date only if it's not already set
                year, month, day = map(int, self.created.split('-'))
                created_date = date(year, month, day)

                # Add 3 days
                due_date = created_date + timedelta(days=3)

                # Store due_date as a string again
                self.due_date = due_date.isoformat() 

        # self.lead_time_days = ((self.recieved_date - self.ordered_date).total_seconds() / 3600)/24
        super().save(*args, **kwargs)

    class Meta():
        verbose_name = 'Bakery Purchase Invoice'
        verbose_name_plural = 'Bakery Purchase Invoice'

    
    @property
    def total_amount(self):
        return self.purchase_total

 


class BakeryPurchaseItems(models.Model):
    purchase_id = models.ForeignKey(BakeryPurchase, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Purchase Id")
    raw_material = models.ForeignKey(RawMaterials, related_name="raw_material_purchase", on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
    quantity = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=200, decimal_places=5, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True,)
    rm_total_qty_kg = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'RM Total Weight (KG)')
    discount_value = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Discount value")
    discount_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Discount Amount")
    net_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Net Amount")
    created = models.DateField(default=now, verbose_name = "Date")
    
    ordered_date = models.DateTimeField( blank=False, null=False, verbose_name="Order Data-Time")
    recieved_date = models.DateTimeField( blank=False, null=False, verbose_name="Received Date-Time")
    lead_time_days = models.DecimalField(max_digits=200, decimal_places=2, default=0)
    class Meta():
        verbose_name = 'Bakery Purchase Item'
        verbose_name_plural = 'Bakery Purchase Items'
    
    @property
    def get_total_qty_kg(self):
        if self.raw_material.entry_measure == "Grams":
            return self.quantity / 1000  # Convert grams to kilograms
        return self.quantity  # If already in kilograms or other measures

    
    @property
    def total_amount(self):
        virtual_qty = 0
        if self.purchase_id:
            return sum([item.get_total_amount for item in self.bakerypurchaseitems_set.all()])
        else:
            return virtual_qty

    @property
    def get_total_returns(self):
        virtual_qty = 0
        if self.purchase_id:
            return sum([item.total_return_amount for item in self.bakeryreturnsitems_set.all()])
        else:
            return virtual_qty

    @property
    def get_discount_total(self):
        virtual_qty = 0
        if self.purchase_id:
            return sum([item.get_discount_value for item in self.bakerypurchaseitems_set.all()])
        else:
            return virtual_qty
    @property
    def get_discount_percentage(self):
        # Default value when invoice_id is not set
        virtual_qty = Decimal('0.00')

        if self.purchase_id:
            # Ensure total_amount is not zero to avoid division by zero
            if self.total_amount == 0:
                return virtual_qty
            return (self.get_discount_total / self.total_amount) * 100
        else:
            return virtual_qty
        
    @property
    def get_grand_total(self):
        virtual_qty = 0
        if self.purchase_id:
            return sum([item.get_total_amount for item in self.bakerypurchaseitems_set.all()]) + self.vat_amount - self.get_total_returns - self.get_discount_total
        else:
            return virtual_qty
        
    

    @property
    def total_amount_paid(self):
        virtual_amount = 0
        if self.purchase_id:
            return sum([item.get_total_amount_paid for item in self.bakerypurchasepayment_set.all()])
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

    # Overriding the save method to update invoice total for each new item
    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        self.discount_value =(self.quantity) *(self.discount_amount)
        self.net_amount = self.total - self.discount_value
        self.rm_total_qty_kg = self.get_total_qty_kg
        # self.lead_time_days = ((self.recieved_date - self.ordered_date).total_seconds() / 3600)/24
        super().save(*args, **kwargs)

class BakeryPurchasePayment(models.Model):
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
    invoice = models.ForeignKey(BakeryInvoice, on_delete=models.SET_NULL, null = True, blank = True,)
    customer = models.ForeignKey(BakeryCustomer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
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
        verbose_name = 'Bakery Purchase Payments'
        verbose_name_plural = 'Bakery Purchase Payments'



# Define the get_latest_price function here
def get_latest_price(raw_material):
    latest_purchase_item = BakeryPurchaseItems.objects.filter(
        raw_material=raw_material
    ).order_by('-purchase_id__recieved_date').first()

    if latest_purchase_item:
        return latest_purchase_item.price
    return 0  # Return a default value if no purchase item is found
#------------------------------------------------------------------------------------------------#
###########   #############   #############   #############   #############
#---------------------------- Bakery Inventory -------------------------#
#############   #############   #############   #############   #############

def increment_inventory_number():
    last_invoice = BakeryInventory.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'BAKINVEN0001'

    invoice_id = last_invoice.inventory_id
    invoice_int = int(invoice_id.split('BAKINVEN000')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'BAKINVEN000'  + str(new_invoice_int)
    return new_invoice_id


class BakeryInventory(models.Model):
    created = models.DateField(default=now, verbose_name = "Date")
    inventory_id = models.CharField(max_length = 500,default=increment_inventory_number, null = True, blank = True, verbose_name="Inventory Id")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    department_name =  models.ForeignKey(Department, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Department')
    total_cost = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.inventory_id)
    
    def get_raw_material_total(self, raw_material):
        return self.bakeryinventoryitems_set.filter(raw_material_name=raw_material).aggregate(total_sum=Sum('total'))['total_sum'] or 0

    
    class Meta():
        verbose_name = 'Bakery Inventory'
        verbose_name_plural = 'Bakery Inventory'


class BakeryInventoryItems(models.Model):
    Status = (
        ('Opening Stock', 'Opening Stock'),
        ('Closing Stock', 'Closing Stock'),
    )

    created = models.DateField(default=now, verbose_name = "Date")
    inventory_id = models.ForeignKey(BakeryInventory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Invoice Id")
    #employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    status =  models.CharField(max_length = 500, choices=Status,  default='Morning', null = True, blank = True )
    raw_material_name = models.ForeignKey(RawMaterials, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    rm_total_qty_kg = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'RM Total Weight (KG)')
    price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True,)

    class Meta():
        verbose_name = 'Bakery Inventory Item'
        verbose_name_plural = 'Bakery Inventory Items'
    
    @property
    def get_total_qty_kg(self):
        if self.raw_material_name.entry_measure == "Grams":
            return self.quantity / 1000  # Convert grams to kilograms
        return self.quantity  # If already in kilograms or other measures

    # Overriding the save method to update invoice total for each new item
    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        self.rm_total_qty_kg = self.get_total_qty_kg
        super().save(*args, **kwargs)


#---------------------- Invoice Number for Invoice Model-------------------#
#--------------------------------------------------------------------------#
###########   #############   #############   #############   #############
#---------------------------- Bakery Inventory -------------------------#
#############   #############   #############   #############   ###########
import datetime
def increment_production_number():
    last_invoice = BakeryProduction.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
        return f"{today_string}-BAKPROD0001"

    invoice_id = last_invoice.production_id
    
    # Check if the last invoice ID starts with today's date
    if today_string in invoice_id:
        # Split the invoice ID to get the number part
        try:
            invoice_int = int(invoice_id.split('BAKPROD')[-1])  # Extract the numeric part
            new_invoice_int = invoice_int + 1
        except (IndexError, ValueError):
            # Handle cases where the split or conversion fails
            new_invoice_int = 1
    else:
        # If the last invoice is from a different day, start with 1 again
        new_invoice_int = 1

    new_invoice_id = f"{today_string}-BAKPROD{new_invoice_int:04d}"

    # Ensure the new ID is unique
    while BakeryProduction.objects.filter(production_id=new_invoice_id).exists():
        new_invoice_int += 1
        new_invoice_id = f"{today_string}-BAKPROD{new_invoice_int:04d}"

    return new_invoice_id


class BakeryProduction(models.Model):
    DEPARTMENTS = (
        ('Bakery', 'Bakery'),
    )

    Sub_Departments = (
        ('Boulangerie', 'Boulangerie'),
        ('Patisserie', 'Patisserie'),
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
    
    created_at = models.DateField("Date", default=now)
    production_id = models.CharField(max_length = 500,default=increment_production_number, null = True, blank = True)
    department =  models.CharField(max_length = 500, choices=DEPARTMENTS, default='Bakery', null = True, blank = True, verbose_name = 'Department')
    sub_department =  models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Sub Department')
    mixture_number =  models.CharField(max_length = 500, choices=MIXTURES, default='', null = True, blank = True, verbose_name = 'Mixture Number')
    session = models.CharField(max_length = 500, choices=SESSIONS, default='', null = True, blank = True, verbose_name = 'Session')
    supervisor =  models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name = 'Supervisor')
    stock_supervisor =  models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name = 'Stock Supervisor')
    total=models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True,  verbose_name = 'Total Cost Price')

    def __str__(self):
        return self.production_id


    class Meta():
                verbose_name = 'Bakery Production'
                verbose_name_plural = 'Bakery Production'


class BakeryRawMaterialUsage(models.Model):

    DIRECT_INDIRECT = (
        ('Direct', 'Direct'),
        ('Indirect', 'Indirect'),
    )


    SESSIONS = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    )
    Status = (
        ('Direct Usage', 'Direct Usage'),
        ('Indirect Usage', 'Indirect Usage'),
    )
    

    production_id = models.ForeignKey(BakeryProduction, null=True, on_delete=models.SET_NULL)
    raw_material = models.ForeignKey(RawMaterials, null=True, on_delete=models.SET_NULL, verbose_name='Raw Material')
    status = models.CharField(max_length = 500, choices=Status, default='', null = True, blank = True, verbose_name = 'Status')
    qty = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0, verbose_name="Quantity Used")
    rm_total_weight_kg = models.DecimalField(max_digits=20, null=True, blank=True, decimal_places=2, default=0, verbose_name='RM Total Weight (KG)')
    unit_cost_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True, verbose_name='Unit Cost Price')
    raw_material_value = models.DecimalField(max_digits=20, null=True, blank=True, decimal_places=2, default=0, verbose_name='Raw Material Value')
    safety_stock = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True, verbose_name='Safety Stock')
    avg_daily_demand = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True, verbose_name='Avg Daily Demand')
    created_at = models.DateField("Date", default=now)
    class Meta():
        verbose_name = 'Bakery Raw Material Usage'
        verbose_name_plural = 'Bakery Raw Material Usage'

    @property
    def get_converted_quantity(self):
        if self.raw_material.entry_measure == "Grams":
            return self.qty / 1000  # Convert grams to kilograms
        return self.qty  # If already in kilograms or other measures
    
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
        # Fetch the latest price for the raw material
        self.unit_cost_price = get_latest_price(self.raw_material)

        # Calculate the raw material value based on the latest price
        self.raw_material_value = self.qty * self.unit_cost_price

        # Calculate the standard deviation of lead time for this raw material
        lead_time_stddev = BakeryPurchaseItems.objects.filter(raw_material=self.raw_material).aggregate(
            stddev_lead_time=StdDev('lead_time_days')
        )['stddev_lead_time']


        # Calculate the average daily demand for this raw material across all records
        self.avg_daily_demand = BakeryRawMaterialUsage.objects.filter(
            raw_material=self.raw_material
        ).aggregate(
            avg_demand=Avg('rm_total_weight_kg')
        )['avg_demand'] or 0

        # Calculate safety stock
        service_level_factor = 1.96  # 95% service level
        if lead_time_stddev and self.avg_daily_demand:
            # Convert Decimal to float for the calculation
            lead_time_stddev_float = float(lead_time_stddev)
            avg_daily_demand_float = float(self.avg_daily_demand)
            
            self.safety_stock = service_level_factor * lead_time_stddev_float * math.sqrt(avg_daily_demand_float)

        # Ensure rm_total_weight_kg is updated
        self.rm_total_weight_kg = self.get_converted_quantity

        # Call the original save method
        super().save(*args, **kwargs)


class BakeryProductionOutput(models.Model):
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

    production_id = models.ForeignKey(BakeryProduction, null=True, on_delete=models.SET_NULL)
    output_category =  models.CharField(max_length = 500, choices=OUTPUTCATEGORY, default='Finished', null = True, blank = True, verbose_name = 'Output Category')
    mixture_number =  models.CharField(max_length = 500, choices=MIXTURES, default='', null = True, blank = True, verbose_name = 'Mixture Number')
    tag =  models.CharField(max_length=200, choices=TAG, default='', verbose_name = 'Product Tag')
    product = models.ForeignKey(BakeryProduct, null=True, on_delete=models.SET_NULL)
    qty = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Quantity')
    product_price = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Price')
    value = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Output Value')
    created = models.DateTimeField(default=now)

    class Meta():
        verbose_name = 'Bakery Production Output'
        verbose_name_plural = 'Bakery Production Output'


    @property
    def get_weight_pack(self):
        return self.raw_material.weight_pack

    def save(self, *args, **kwargs):
        self.value   = self.qty * self.product_price
        super().save(*args, **kwargs)

class BakeryConsumptionDamages(models.Model):
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

    production_id = models.ForeignKey(BakeryProduction, null = True, blank = True, on_delete=models.SET_NULL)
    status =  models.CharField(max_length = 500, choices=STATUS, default='', null = True, blank = True, verbose_name = 'Status')
    sub_department =  models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Sub Department')
    session = models.CharField(max_length = 500, choices=SESSIONS, default='', null = True, blank = True, verbose_name = 'Session')
    employee = models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name = 'Employee')
    product = models.ForeignKey(BakeryProduct, null=True, on_delete=models.SET_NULL)
    qty = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Quantity')
    product_price = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Price')
    value = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Output Value')
    created_at = models.DateField("Date", default=now)
    class Meta():
        verbose_name = 'Bakery Consumption & Damages'
        verbose_name_plural = 'Bakery Consumption & Damages'

    #@property
    #def get_weight_pack(self):
        #return self.raw_material.weight_pack


    def save(self, *args, **kwargs):
        self.value   = self.qty * self.product_price
        super().save(*args, **kwargs)


class BakeryProductUnitWeight(models.Model):
    product = models.ForeignKey(BakeryProduct, null=True, on_delete=models.CASCADE)
    weight_per_boul = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    output_per_boul = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    product_unit_weight = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.product_unit_weight = self.weight_per_boul / self.output_per_boul
        super().save(*args, **kwargs)

    class Meta():
        verbose_name = 'Bakery Product Unit Weight'
        verbose_name_plural = 'Bakery Product Unit Weights'

