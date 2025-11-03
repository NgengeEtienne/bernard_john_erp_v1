from django import forms
from .models import *


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"
        exclude = ('slug',)
