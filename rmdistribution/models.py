from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings
from django.template.defaultfilters import slugify
import datetime

from product.models import *
from configuration.models import *
from inventory.models import *
# Create your models here.

#------------------------------------------------------------------------------------------------#
def increment_rmdistribution_number():
    last_invoice = RmDistribution.objects.all().order_by('id').last()
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    if not last_invoice:
            return today_string + "-" + 'DISTRI0001'

    invoice_id = last_invoice.distribution_id
    invoice_int = int(invoice_id.split('DISTRI000')[-1])
    new_invoice_int = invoice_int + 1

    new_invoice_id = today_string + "-" + 'DISTRI000'  + str(new_invoice_int)
    return new_invoice_id


class RmDistribution(models.Model):
    created = models.DateField(default=now, verbose_name = "Date")
    distribution_id = models.CharField(max_length = 500,default=increment_rmdistribution_number, null = True, blank = True, verbose_name="Customer Name")
    employee = models.CharField(max_length = 500,  default='', null = True, blank = True, verbose_name="employee")
    sub_department =  models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, default='', null = True, blank = True, verbose_name = 'Sub Department')



    def __str__(self):
        return str(self.distribution_id)

    class Meta():
        verbose_name = 'Rm Distribution Invoice'
        verbose_name_plural = 'Rm Distribution Invoice'

#------------------------------------------------------------------------------------------------#
class RmDistributionItems(models.Model):
    Status = (
        ('Added Stock', 'Added Stock'),
        ('Transfer Inwards', 'Transfer Inwards'),
        ('Transfer Outwards', 'Transfer Outwards'),
    )
    created = models.DateField(default=now, verbose_name = "Date")
    distribution_id = models.ForeignKey(RmDistribution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Invoice Id")
    status =  models.CharField(max_length = 500, choices=Status,  default='Morning', null = True, blank = True )
    raw_material = models.ForeignKey(RawMaterials, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product Name")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=0, default=0, blank=True, null=True,)

    class Meta():
        verbose_name = 'Rm Distribution Items'
        verbose_name_plural = 'Rm Distribution Items'

    # Overriding the save method to update invoice total for each new item
    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        #self.total_amount = order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
        #self.invoice.save()
        super().save(*args, **kwargs)

#------------------------------------------------------------------------------------------------#
