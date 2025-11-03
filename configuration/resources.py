from inspect import Attribute
from tkinter import Widget
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget,DateWidget
from .models import *
from configuration import *



class SubDepatmentAdminResource(resources.ModelResource):
    department_name = fields.Field(column_name='department_name', attribute='department_name',
                            widget=ForeignKeyWidget(Department, field='department_name'))
    class Meta:
        model = SubDepartment
        fields = ( 'id', 'id', 'department_name', 'sub_department_name' )

