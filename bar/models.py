from django.db import models
from django.template.defaultfilters import slugify
# import datetime
from decimal import Decimal
from django.urls import reverse
from django.utils.timezone import now
from configuration.models import *
from django.core.validators import RegexValidator, MinValueValidator
import uuid
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Sum
from datetime import datetime, timedelta,date
import datetime


#############   #############   #############   #############   #############
#------------------------- Product / Category ------------------------------#
#############   #############   #############   #############   #############

class BarProductCategory(models.Model):
    category_name = models.CharField(max_length=100, default='', verbose_name = "Category Name")


    def __str__(self):
        return str(self.category_name)

    class Meta:
        verbose_name = 'Bar Product Category'
        verbose_name_plural = 'Bar Product Category'


class BarProduct(models.Model):
    product_name = models.CharField(max_length=100, default='', unique=True, verbose_name = "Product Name")
    category = models.ForeignKey(BarProductCategory, on_delete=models.SET_NULL, default=1, null = True, blank = True, verbose_name = "Category")
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name = "Supply Price")
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True, verbose_name = "Selling Price")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    unit_measure = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True, verbose_name = "Litres/grams")


    def __str__(self):
        return str(self.product_name)

    def get_absolute_url(self):
        return reverse('product_name:product-details', args=[self.slug])

    def save(self, *args, **kwargs):
            self.slug = slugify(self.product_name)
            super(BarProduct, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'Bar Product'
        verbose_name_plural = 'Bar Products'


#############   #############   #############   #############   #############
    #------------------------- Inventory --------------------------------#
#############   #############   #############   #############   #############

def increment_inventory_number():
    last_invoice = BarInventory.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'BAR-INVEN0001'

    invoice_id = last_invoice.inventory_id
    invoice_int = int(invoice_id.split('BAR-INVEN000')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'BAR-INVEN000'  + str(new_invoice_int)
    return new_invoice_id

class BarInventory(models.Model):
    created = models.DateField(default=now, verbose_name = "Date")
    inventory_id = models.CharField(max_length = 500,default=increment_inventory_number, null = True, blank = True, verbose_name="Inventory Id")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="Stock Person")
    description = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="Description")
    total_price = models.DecimalField(max_digits=20, decimal_places=0, default=0.0, blank=True, null=True, verbose_name="Total Price")

    def __str__(self):
        return str(self.inventory_id)

    class Meta():
        verbose_name = 'Bar Inventory'
        verbose_name_plural = 'Bar Inventory'

 
class BarInventoryItems(models.Model):
    Status = (
        ('Opening Stock', 'Opening Stock'),
        ('Added Stock', 'Added Stock'),
        ('Closing Stock', 'Closing Stock'),
        ('Damages', 'Damages'),
        ('Returns Outwards', 'Returns Outwards'),
        ('Returns Inwards', 'Returns Inwards'),
    )
    created = models.DateField(default=now, verbose_name = "Date")
    inventory_id = models.ForeignKey(BarInventory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Inventory Id")
    # employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    status =  models.CharField(max_length = 500, choices=Status,  default='Morning', null = True, blank = True )
    product_name = models.ForeignKey(BarProduct, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    cost_price = models.DecimalField(max_digits=20, decimal_places=0, default=0, verbose_name="Cost Price")
    selling_price = models.DecimalField(max_digits=20, decimal_places=0, default=0, verbose_name="Selling Price")
    total_cost_price = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True, verbose_name="Total Cost Price")
    total_selling_price = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True, verbose_name="Total Selling Price")

    class Meta():
        verbose_name = 'Bar Inventory Item'
        verbose_name_plural = 'Bar Inventory Items'

    # Overriding the save method to update invoice total for each new item
    def save(self, *args, **kwargs):
        self.total_cost_price = self.quantity * self.cost_price
        self.total_selling_price = self.quantity * self.selling_price
        #self.total_amount = order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
        #self.invoice.save()
        super().save(*args, **kwargs)
        
        
    
#############   #############   #############   #############   #############
#---------------------------- Purchases -------------------------#
#############   #############   #############   #############   #############

#------------------------- Bar Suppliers ---------------------#


phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message='Phone number invalid. Should start with example: +237'
)

class BarSupplier(models.Model):

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
        verbose_name = ' Bar Suppliers'
        verbose_name_plural = 'Bar Suppliers'

    def __str__(self):
        return "{}".format(self.supplier_name)


    def get_absolute_url(self):
        return reverse('supplier:supplier-details', args=[self.slug])

    def save(self, *args, **kwargs):
            self.slug = slugify(self.supplier_name)
            super(BarSupplier, self).save(*args, **kwargs)

    #class Meta:
        #ordering = ['-created']

#------------------------- Bar Pruchase Summary---------------------#
class BarPurchaseSummary(models.Model):
    SubDepartment = (
        ('Boulangerie Morning', 'Boulangerie Morning'),
        ('Boulangerie Evening', 'Boulangerie Evening'),
        ('Patisserie', 'Patisserie'),
        ('Magazine', 'Magazine'),
    )
    created = models.DateField(default=now, verbose_name = "Date")
    purchase_id = models.CharField(max_length = 500,default='', null = True, blank = True, verbose_name="Purchase ID")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    supplier_name = models.ForeignKey(BarSupplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Supplier's Name")
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

        return super(BarPurchaseSummary, self).save(*args, **kwargs)


    class Meta():
        verbose_name = 'Bar Purchase Summary'
        verbose_name_plural = 'Bar Purchase Summary'
        
def increment_purchase_number():
    last_invoice = BarPurchase.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'BAR-PUR-001'

    invoice_id = last_invoice.purchase_id
    invoice_int = int(invoice_id.split('BAR-PUR-00')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'BAR-PUR-00'  + str(new_invoice_int)
    return new_invoice_id 


class BarPurchase(models.Model):
    SubDepartment = (
    ('Boulangerie Morning', 'Boulangerie Morning'),
    ('Boulangerie Evening', 'Boulangerie Evening'),
    ('Patisserie', 'Patisserie'),
    ('Magazine', 'Magazine'),
)
    Statustag = (
        ('Purchases', 'Purchases'),
        ('Return Outwards', 'Return Outwards'),
       
    ) 
    created = models.DateField(default=now, verbose_name = "Date")
    purchase_id = models.CharField(max_length = 500,default=increment_purchase_number, null = True, blank = True, verbose_name="Customer Name")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    supplier_name = models.ForeignKey(BarSupplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Supplier's Name")
    sub_department =  models.CharField(max_length = 500, choices=SubDepartment,  default='Morning', null = True, blank = True)
    due_date = models.DateField(null=True, blank=True, verbose_name = "Due Date")
    purchase_total = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Purchase Total")
    vat_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="VAT Amount")
    discount_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Discount Amount")
    net_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Net Amount")
    status =  models.CharField(max_length = 500, choices=Statustag,  default='Purchases', null = True, blank = True)
    def __str__(self):
        return str(self.purchase_id)
    
    def save(self, *args, **kwargs):
        # Automatically set the due date to 3 days from the creation date if not provided
        if not self.due_date:
            year, month, day = map(int, self.created.split('-'))
            created_date = date(year, month, day)

            # Add 3 days
            self.due_date = created_date + timedelta(days=3)

        # Calculate the net amount
        self.net_amount = float(self.purchase_total) - float(self.discount_amount) + float(self.vat_amount)

        # Call the parent save method
        super(BarPurchase, self).save(*args, **kwargs)

    class Meta():
        verbose_name = 'Bar Purchase Invoice'
        verbose_name_plural = 'Bar Purchase Invoice'

class BarPurchaseItems(models.Model):
    purchase_id = models.ForeignKey(BarPurchase, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Purchase ID")
    product_name = models.ForeignKey(BarProduct, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, default=0, verbose_name="Quantity")
    cost_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name="Cost Price")
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name="Selling Price")
    discount_value = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Discount value")
    discount_amount = models.DecimalField(default=0, max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Discount Amount")
    total_cost_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True, null=True, verbose_name="Total Cost Price")
    total_selling_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True, null=True, verbose_name="Total Selling Price")
    gross_profit = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True, null=True, verbose_name="Gross Profit")

    class Meta:
        verbose_name = 'Bar Purchase Item'
        verbose_name_plural = 'Bar Purchase Items'

    def save(self, *args, **kwargs):
        # Ensure that quantity, cost_price, and selling_price are not None to avoid any NoneType errors
        if self.quantity is None:
            self.quantity = 0
        if self.cost_price is None:
            self.cost_price = 0
        if self.selling_price is None:
            self.selling_price = 0
        if self.discount_amount is None:
            self.discount_amount = 0

        # Calculate total cost price
        self.total_cost_price = self.quantity * self.cost_price

        # Calculate discount value
        self.discount_value = self.quantity * self.discount_amount

        # Calculate total selling price
        self.total_selling_price = (self.quantity * self.selling_price) - Decimal(self.discount_value)

        # Calculate gross profit
        self.gross_profit = self.total_selling_price - self.total_cost_price

        # Call the superclass save method to save the changes
        super().save(*args, **kwargs)

        # Update the purchase total for the parent BarPurchase
        if self.purchase_id:
            total_purchase = BarPurchaseItems.objects.filter(purchase_id=self.purchase_id).aggregate(total_cost_price=Sum('total_cost_price'))['total_cost_price'] or 0
            self.purchase_id.purchase_total = total_purchase
            self.purchase_id.save()  # Ensure the parent purchase total is saved

    def delete(self, *args, **kwargs):
        purchase = self.purchase_id
        super().delete(*args, **kwargs)  # Delete the item

        # Update the purchase total after deletion
        if purchase:
            total_purchase = BarPurchaseItems.objects.filter(purchase_id=purchase).aggregate(total_cost_price=Sum('total_cost_price'))['total_cost_price'] or 0
            purchase.purchase_total = total_purchase
            purchase.save()  # Save the updated total
#------------------------------------------------------------------------------------------------#

def increment_invoice_number():
    last_invoice_payment = BarPurchasePayment.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice_payment:
            return today_string + "-" + 'BARPAYMT0001'

    payment_id = last_invoice_payment.payment_id
    payment_int = int(payment_id.split('BARPAYMT000')[-1])
    new_payment_int = payment_int + 1

    new_payment_id = today_string + "-" + 'BARPAYMT000'  + str(new_payment_int)
    return new_payment_id


#############   #############   #############   #############   #############
#------------------------- Boulangerie Payment ---------------------#
#############   #############   #############   #############   #############
class BarPurchasePayment(models.Model):
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
    invoice = models.ForeignKey(BarPurchase, on_delete=models.SET_NULL, null = True, blank = True,)
    #payment_id = models.CharField(max_length = 500,default=increment_invoice_number, null = True, blank = True)
    customer = models.ForeignKey(BarSupplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Customer Name")
    payment_installment =  models.CharField(max_length = 500, choices=Payment_Installment,  default='1st Installment', null = True, blank = True)
    employee = models.CharField(max_length = 500, null = True, blank = True, default='')
    amount_paid = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    

    def __str__(self):
        return self.payment_installment

    @property
    def get_total_amount_paid(self):
        return self.amount_paid

    class Meta():
        verbose_name = 'Boulangerie Customers Payments'
        verbose_name_plural = 'Boulangerie Customers Payments'
     