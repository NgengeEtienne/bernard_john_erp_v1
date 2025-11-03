from django.urls import path
from . import views

app_name = 'supplier'


urlpatterns = [
    path('', views.suppliers_view, name='supplier'),
    path('create-supplier/', views.add_supplier.as_view(), name='create-supplier'),
    path('edit-supplier/<int:pk>/', views.edit_supplier.as_view(), name='edit-supplier'),
    path('supplier-details/<slug:slug>/', views.supplier_details, name='supplier-details'),

]
