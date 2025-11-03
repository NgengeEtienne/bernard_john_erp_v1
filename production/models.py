from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.timezone import now
import datetime

from configuration.models import *
from inventory.models import *
from product.models import *

# Create your models here.
#---------------------- Invoice Number for Invoice Model----------------------#

def increment_production_number():
    last_invoice = Production.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'PROD0001'

    invoice_id = last_invoice.production_id
    invoice_int = int(invoice_id.split('PROD000')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'PROD000'  + str(new_invoice_int)
    return new_invoice_id


class Production(models.Model):
    DEPARTMENTS = (
        ('Bakery', 'Bakery'),
    )

    SUBDEPARTMENTS = (
        ('Boulangerie Morning', 'Boulangerie Morning'),
        ('Boulangerie Evening', 'Boulangerie Evening'),
        ('Patisserie Morning', 'Patisserie Morning'),
        ('Patisserie Evening', 'Patisserie Evening'),
        ('All', 'All'),

    )

    SESSIONS = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    )

    created_at = models.DateField("Date", default=now)
    production_id = models.CharField(max_length = 500,default=increment_production_number, null = True, blank = True)
    department =  models.CharField(max_length = 500, choices=DEPARTMENTS, default='Bakery', null = True, blank = True, verbose_name = 'Department')
    sub_department =  models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Sub Department')
    session = models.CharField(max_length = 500, choices=SESSIONS, default='', null = True, blank = True, verbose_name = 'Session')
    supervisor =  models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name = 'Supervisor')


    def __str__(self):
        return self.production_id


    class Meta():
                verbose_name = 'Production'
                verbose_name_plural = 'Production'


class RawMaterialUsage(models.Model):

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

    production_id = models.ForeignKey(Production, null=True, on_delete=models.SET_NULL)
    mixture_number =  models.CharField(max_length = 500, choices=MIXTURES, default='', null = True, blank = True, verbose_name = 'Mixture Number')
    raw_material = models.ForeignKey(RawMaterials, null=True, on_delete=models.SET_NULL, verbose_name = 'Raw Material')
    qty = models.DecimalField(max_digits=20, decimal_places=2, null = True, blank = True, default=0, verbose_name="Quantity Used")
    rm_total_weight_grams = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'RM Total Weight (Grams)')
    unit_cost_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True,  verbose_name = 'Unit Cost Price')
    raw_material_value = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Raw Material Value')


    class Meta():
        verbose_name = 'Raw Material Usage'
        verbose_name_plural = 'Raw Material Usage'

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


class ProductionOutput(models.Model):
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

    production_id = models.ForeignKey(Production, null=True, on_delete=models.SET_NULL)
    output_category =  models.CharField(max_length = 500, choices=OUTPUTCATEGORY, default='Finished', null = True, blank = True, verbose_name = 'Output Category')
    mixture_number =  models.CharField(max_length = 500, choices=MIXTURES, default='', null = True, blank = True, verbose_name = 'Mixture Number')
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    qty = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Quantity')
    product_price = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Price')
    value = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Output Value')


    class Meta():
        verbose_name = 'Production Output'
        verbose_name_plural = 'Production Output'


    @property
    def get_weight_pack(self):
        return self.raw_material.weight_pack

    def save(self, *args, **kwargs):
        self.value   = self.qty * self.product_price
        super().save(*args, **kwargs)

class ConsumptionDamages(models.Model):
    STATUS = (
        ('Consumption', 'Consumption'),
        ('Damages', 'Damages'),
        ('Opening Stock', 'Opening Stock'),
        ('Closing Stock', 'Closing Stock'),
    )
    production_id = models.ForeignKey(Production, null = True, blank = True, on_delete=models.SET_NULL)
    status =  models.CharField(max_length = 500, choices=STATUS, default='', null = True, blank = True, verbose_name = 'Status')
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    qty = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Quantity')
    product_price = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Price')
    value = models.DecimalField(max_digits=20, null = True, blank = True, decimal_places=2, default=0, verbose_name = 'Output Value')


    class Meta():
        verbose_name = 'Consumption & Damages'
        verbose_name_plural = 'Consumption & Damages'

    #@property
    #def get_weight_pack(self):
        #return self.raw_material.weight_pack


    def save(self, *args, **kwargs):
        self.value   = self.qty * self.product_price
        super().save(*args, **kwargs)
