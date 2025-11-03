from __future__ import unicode_literals
from django.db import models
from decimal import Decimal
from django.urls import reverse
from django.core.validators import RegexValidator, MinValueValidator
import uuid
import datetime
from django.utils.timezone import now
from django.template.defaultfilters import slugify

from django.db.models.signals import post_save
from django.db.models import Sum

# Create your models here.

# phone validator using regular expressions
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message='Phone number invalid. Should start with example: +237'
)

class Supplier(models.Model):

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
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'

    def __str__(self):
        return "{}".format(self.supplier_name)


    def get_absolute_url(self):
        return reverse('supplier:supplier-details', args=[self.slug])

    def save(self, *args, **kwargs):
            self.slug = slugify(self.supplier_name)
            super(Supplier, self).save(*args, **kwargs)

    #class Meta:
        #ordering = ['-created']
