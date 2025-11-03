from django import forms
from .models import *

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        exclude = ('slug',)
        widgets = {
            'created': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'instruction1': forms.TextInput(attrs={'class': 'form-control'}),
            'instruction2': forms.TextInput(attrs={'class': 'form-control'}),
            'instruction3': forms.TextInput(attrs={'class': 'form-control'}),
            'instruction4': forms.TextInput(attrs={'class': 'form-control'}),
            'instruction5': forms.TextInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }

