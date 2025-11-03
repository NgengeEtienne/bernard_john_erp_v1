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

class Customer(models.Model):

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
    street = models.CharField(max_length=300, choices=Street_Location, null = True, blank = True, verbose_name = "Street")
    street_location = models.CharField(max_length=30, choices=Street_Location, null = True, blank = True, verbose_name = "Own Company Box")
    address = models.TextField(max_length=2550, null=True, verbose_name = "Address")
    city = models.CharField(max_length=100, default='Kumba', verbose_name = "City")
    region = models.CharField(max_length=200, default='South West Region', verbose_name = "Region")
    phone = models.CharField(validators=[phone_regex], max_length=15, null=True, blank = True, verbose_name = "Phone +237")
    email = models.EmailField(blank=True, null=True, verbose_name = "Email")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True,default=0.0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True,default=0.0)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return "{}".format(self.customer_name)


    def get_absolute_url(self):
        return reverse('customer:customer-details', args=[self.slug])

    def save(self, *args, **kwargs):
            self.slug = slugify(self.customer_name)
            super(Customer, self).save(*args, **kwargs)

    #class Meta:
        #ordering = ['-created']
