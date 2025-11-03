from inspect import Attribute
from tkinter import Widget
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget,DateWidget
from .models import *
from inventory.models import *

class ProductionAdminResource(resources.ModelResource):
    sub_department = fields.Field(column_name='sub_department', attribute='sub_department',
                        widget=ForeignKeyWidget(SubDepartment, field='department_name'))

    class Meta:
        model = Production
        fields = (
            'id', 'created_at', 'production_id','department', 'sub_department', 'session', 'supervisor',
                    )

class RawMaterialUsageAdminResource(resources.ModelResource):
    production_id = fields.Field(column_name='production_id', attribute='production_id',
                        widget=ForeignKeyWidget(Production, field='production_id'))

    raw_material = fields.Field(column_name='raw_material', attribute='raw_material',
                        widget=ForeignKeyWidget(RawMaterials, field='product'))

    class Meta:
        model = RawMaterialUsage
        fields = (
            'id',  'production_id', 'mixture_number', 'raw_material', 'qty', 'rm_total_weight_grams',
            'unit_cost_price', 'raw_material_value',
        )

#--------------------------------------------------------------------------------------------------------#

class ProductionOutputAdminResource(resources.ModelResource):
    production_id = fields.Field(column_name='production_id', attribute='production_id',
                        widget=ForeignKeyWidget(Production, field='production_id'))

    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(Product, field='product_name'))

    class Meta:
        model = ProductionOutput
        fields = (
            'id', 'production_id','mixture_number', 'output_category', 'product', 'qty', 'product_price', 'value'
        )

class ConsumptionDamagesAdminResource(resources.ModelResource):
    production_id = fields.Field(column_name='production_id', attribute='production_id',
                        widget=ForeignKeyWidget(Production, field='production_id'))

    product = fields.Field(column_name='product', attribute='product',
                        widget=ForeignKeyWidget(Product, field='product_name'))

    class Meta:
        model = ConsumptionDamages
        fields = (
            'id', 'production_id','status', 'product', 'qty', 'product_price', 'value'
        )
