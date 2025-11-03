from django.db import models
from django.template.defaultfilters import slugify
import datetime
from django.utils.timezone import now


# Create your models here.
class Department(models.Model):
    department_name = models.CharField(max_length=100, default='')

    def __str__(self):
        return str(self.department_name)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

class Category(models.Model):
    category_name = models.CharField(max_length=100, default='')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank =True)


    def __str__(self):
        return str(self.category_name)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    product_name = models.CharField(max_length=100, default='', unique=True, verbose_name = "Product Name")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, default=1, null = True, blank = True, verbose_name = "Category")
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True, verbose_name = "Selling Price Pos")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    entry_weight_per_boule = models.CharField(max_length=100, default='', verbose_name = "Entry Weight/Boule")
    weight_per_boule_kg = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True, verbose_name = "Weight/Boule/kg")
    weight_per_boule_gram = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True, verbose_name = "Weight/Boule/grams")
    output_per_boule = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True, verbose_name = "Output/Boule")
    unit_output_weight = models.DecimalField(max_digits=20, decimal_places=2, default=0, null = True, blank = True, verbose_name = "Weight/Unit Output/grams")




    def __str__(self):
        return str(self.product_name)

    def get_absolute_url(self):
        return reverse('product:product-details', args=[self.slug])

    def save(self, *args, **kwargs):
            self.slug = slugify(self.product_name)
            super(Product, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
