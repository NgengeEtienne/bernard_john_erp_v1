
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget,DateWidget
from .models import *
from product.models import *
from configuration.models import *


class InventoryAdminResource(resources.ModelResource):
    sub_department = fields.Field(column_name='sub_department', attribute='sub_department',
                        widget=ForeignKeyWidget(SubDepartment, field='department_name'))


    class Meta:
        model = Inventory
        fields = (
            'id', 'created', 'inventory_id', 'employee', 'sub_department',
        )

class InventoryItemsAdminResource(resources.ModelResource):
    inventory_id = fields.Field(column_name='inventory_id', attribute='inventory_id',
                        widget=ForeignKeyWidget(Inventory, field='inventory_id'))

    sub_department = fields.Field(column_name='sub_department', attribute='sub_department',
                        widget=ForeignKeyWidget(SubDepartment, field='department_name'))

    raw_material= fields.Field(column_name='raw_material', attribute='raw_material',
                        widget=ForeignKeyWidget(RawMaterials, field='product'))
    class Meta:
        model = InventoryItems
        fields = (
            'id', 'created', 'inventory_id', 'sub_department', 'employee', 'status', 'raw_material', 'quantity', 'price', 'total',
        )
