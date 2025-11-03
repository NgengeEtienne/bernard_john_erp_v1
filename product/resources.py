from inspect import Attribute
from tkinter import Widget
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget,DateWidget
from .models import *


class CategoryAdminResource(resources.ModelResource):
    department = fields.Field(column_name='department', attribute='department',
                            widget=ForeignKeyWidget(Department, field='department_name'))
    class Meta:
        model = Category
        fields = ( 'id', 'category_name', 'department', )

class ProductAdminResource(resources.ModelResource):
    category = fields.Field(column_name='category', attribute='category',
                        widget=ForeignKeyWidget(Category, field='category_name'))
    class Meta:
        model = Product
        fields = (
            'id','created','product_name', 'category', 'price', 'selling_price', 'slug',
            "entry_weight_per_boule", 'weight_per_boule_kg', 'weight_per_boule_gram', 'output_per_boule',
    'unit_output_weight'
        )
