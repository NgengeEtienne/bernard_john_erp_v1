from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings
from django.template.defaultfilters import slugify
import datetime

from product.models import *
from configuration.models import *
# Create your models here.
#------------------------------------------------------------------------------------------------#
class RawMaterials(models.Model):
    CATEGORY = (
        ('Direct', 'Direct'),
        ('Indirect', 'Indirect'),
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

    product =  models.CharField(max_length = 500, default='', null = True, blank = True, verbose_name = 'Product Name')
    category=  models.CharField(max_length = 500, choices=CATEGORY, default='Direct', null = True, blank = True, verbose_name = 'Category')
    weight_pack =   models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank=True, verbose_name = 'Weight/Pack')
    entry_measure =  models.CharField(max_length=200, choices=ENTRYMEASURE, verbose_name = 'Entry Measure')
    packaging =  models.CharField(max_length = 500, default='', choices=PACKAGING, null = True, blank = True, verbose_name = 'Packaging')


    def __str__(self):
        return self.product

    class Meta():
        verbose_name = 'Raw Material'
        verbose_name_plural = 'Raw Materials'

#------------------------------------------------------------------------------------------------#
def increment_inventory_number():
    last_invoice = Inventory.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'INVEN0001'

    invoice_id = last_invoice.inventory_id
    invoice_int = int(invoice_id.split('INVEN000')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'INVEN000'  + str(new_invoice_int)
    return new_invoice_id


class Inventory(models.Model):
    created = models.DateField(default=now, verbose_name = "Date")
    inventory_id = models.CharField(max_length = 500,default=increment_inventory_number, null = True, blank = True, verbose_name="Inventory Id")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    sub_department =  models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Sub Department')



    def __str__(self):
        return str(self.inventory_id)

    class Meta():
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventory'

#------------------------------------------------------------------------------------------------#
class InventoryItems(models.Model):
    Status = (
        ('Opening Stock', 'Opening Stock'),
        ('Added Stock', 'Added Stock'),
        ('Transfer Inwards', 'Transfer Inwards'),
        ('Transfer Outwards', 'Transfer Outwards'),
        ('Closing Stock', 'Closing Stock'),
    )
    created = models.DateField(default=now, verbose_name = "Date")
    inventory_id = models.ForeignKey(Inventory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Invoice Id")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    status =  models.CharField(max_length = 500, choices=Status,  default='Morning', null = True, blank = True )
    raw_material = models.ForeignKey(RawMaterials, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True,)

    class Meta():
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'

    # Overriding the save method to update invoice total for each new item
    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        #self.total_amount = order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
        #self.invoice.save()
        super().save(*args, **kwargs)

#------------------------------------------------------------------------------------------------#
'''
def increment_invoice_number():
    last_invoice = FinishedProductInventoryItems.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'FinPr0001'

    invoice_id = last_invoice.finished_product_inventory_id
    invoice_int = int(invoice_id.split('FinPr000')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'FinPr000'  + str(new_invoice_int)
    return new_invoice_id
'''