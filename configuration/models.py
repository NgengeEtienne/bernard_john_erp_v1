from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.template.defaultfilters import slugify
import uuid
import datetime

class Department(models.Model):
    DEPARTMENTS = (
        ('Supermarket', 'Supermarket'),
        ('Bakery', 'Bakery'),
        ('Boulangerie', 'Boulangerie'),
        ('Bar', 'Bar'),
        ('WholeSale', 'WholeSale'),
        ('Ice Cream', 'Ice Cream'),

    )

    #created_at = models.DateField("Date", default=now)
    department_name =  models.CharField(max_length = 500, choices=DEPARTMENTS, default='', null = True, blank = True, verbose_name = 'Employee')

    #def get_absolute_url(self):
        #return reverse('expenses:expense-payables-details', args=[self.slug])

    def __str__(self):
        return self.department_name

    class Meta():
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        #ordering: ['-created_at']


class SubDepartment(models.Model):
    SUBDEPARTMENTS = (
        ('Boulangerie', 'Boulangerie'),
        ('Patisserie', 'Patisserie'),
        ('Magazine', 'Magazine'),

    )

    #created_at = models.DateField("Date", default=now)
    department_name = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Dapartment")
    sub_department_name =  models.CharField(max_length = 500, choices=SUBDEPARTMENTS, default='', null = True, blank = True, verbose_name = 'Sub Department')

    #def get_absolute_url(self):
        #return reverse('expenses:expense-payables-details', args=[self.slug])

    def __str__(self):
        return self.sub_department_name

    class Meta():
        verbose_name = 'Sub Department'
        verbose_name_plural = 'Sub Departments'
        #ordering: ['-created_at']

class Session(models.Model):
    SESSIONS = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    )

    #created_at = models.DateField("Date", default=now)
    session_name =  models.CharField(max_length = 500, choices=SESSIONS, default='', null = True, blank = True, verbose_name = 'Employee')

    #def get_absolute_url(self):
        #return reverse('expenses:expense-payables-details', args=[self.slug])

    def __str__(self):
        return self.session_name

    class Meta():
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'
        #ordering: ['-created_at']


class ManagementLevel(models.Model):
    Levels = (
        ('Management', 'Management'),
        ('Employee', 'Employee'),
    )

    #created_at = models.DateField("Date", default=now)
    management_level =  models.CharField(max_length = 500, choices=Levels, default='', null = True, blank = True, verbose_name = 'Employee')

    #def get_absolute_url(self):
        #return reverse('expenses:expense-payables-details', args=[self.slug])

    def __str__(self):
        return self.management_level

    class Meta():
        verbose_name = 'Management Level'
        verbose_name_plural = 'Management Level'
        #ordering: ['-created_at']