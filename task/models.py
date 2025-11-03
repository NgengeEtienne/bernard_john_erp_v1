from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.template.defaultfilters import slugify
import uuid


class Author(models.Model):
    # Here we use a OneToOne Relationship because it allows us to create One user to an Employee
    # Whereas a ForeignKey allows us to create many users for one Employee
    author= models.CharField(max_length=500, default="", blank=True, null=True)
    images = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.author

class Employee(models.Model):
    # Here we use a OneToOne Relationship because it allows us to create One user to an Employee
    # Whereas a ForeignKey allows us to create many users for one Employee
    employee = models.CharField(max_length=500, default="", blank=True, null=True)
    images = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.employee

class Task(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )

    PRIORITYLEVELS = (
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('Critical', 'Critical'),
    )

    DEPARTMENTS= (
        ('Bakery', 'Bakery'),
        ('Boulangerie', 'Boulangerie'),
        ('Bar', 'Bar'),
        ('Snack', 'Snack'),
        ('Ice Cream', 'Ice Cream'),
        ('Supermarket', 'Supermarket'),
    )
    created = models.DateField("Date", default=now)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=100, unique=True, default=uuid.uuid4, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    department = models.CharField(max_length=300, choices = DEPARTMENTS, default='')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    description = models.TextField(max_length=500)
    instruction1 = models.CharField(max_length=200, blank=True, null=True)
    instruction2 = models.CharField(max_length=200, blank=True, null=True, default='')
    instruction3 = models.CharField(max_length=200, blank=True, null=True, default='')
    instruction4 = models.CharField(max_length=200, blank=True, null=True, default='')
    instruction5 = models.CharField(max_length=200, blank=True, null=True, default='')
    comments = models.TextField(max_length=500, blank=True, null=True , default='')
    state = models.CharField(max_length=300, choices = STATUS, default='')
    priority =  models.CharField(max_length=300, choices = PRIORITYLEVELS, default='')
    #completion_status = models.BooleanField(default= False)
    expiry_date = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)


    def get_absolute_url(self):
        return reverse('task:task-detail', args=[self.slug])

    def __str__(self):
        return self.title

    @property
    def get_duration(self):
        created = self.created_at
        expiry_date = self.expiry_date
        if created:
            return expiry_date - created
        return

    class Meta:
        ordering = ['-created']
