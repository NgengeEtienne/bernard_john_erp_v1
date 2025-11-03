from django.urls import path
from . import views
from .views import SupermarketCustomerListView, SupermarketCustomerDetailView, SupermarketCustomerCreateView, SupermarketCustomerEditView
from .views import (
    SupermarketProductCategoryListView,
    SupermarketProductCategoryDetailView,
    SupermarketProductCategoryCreateView,
    SupermarketProductCategoryEditView,
)
app_name = 'supermarket'




urlpatterns = [
     path('', views.view, name='supermarket'),
    # Customers
    path('customers/', SupermarketCustomerListView.as_view(), name='customer-list'),
    path('customers/add/', SupermarketCustomerCreateView.as_view(), name='customer-add'),
    path('customers/<slug:slug>/', SupermarketCustomerDetailView.as_view(), name='customer-detail'),
    path('customers/<slug:slug>/edit/', SupermarketCustomerEditView.as_view(), name='customer-edit'),

    # Categories
    path('categories/', SupermarketProductCategoryListView.as_view(), name='category-list'),
    path('categories/add/', SupermarketProductCategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', SupermarketProductCategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/edit/', SupermarketProductCategoryEditView.as_view(), name='category-edit'),

    # Invoices
    path('invoices/', views.invoice_view, name='invoice'),
    path('invoices/create/', views.create_invoice, name='create-invoice'),
    path('invoices/<int:pk>/view/', views.invoice_detail, name='view_invoice_detail'),
    path('invoices/<int:pk>/edit/', views.edit_invoice, name='edit_invoice'),
    # ... other invoice-related URLs

    # Purchases
    path('purchases/', views.purchases_view, name='purchases'),
    path('purchases/create/', views.create_purchase, name='create-purchase'),
    path('purchases/<int:pk>/view/', views.purchase_detail, name='purchase_detail'),
    path('purchases/edit/<int:pk>/', views.edit_purchase, name='edit-purchase'),

    # ... other purchase-related URLs

    # Suppliers
    path('suppliers/', views.suppliers_view, name='supplier'),
    path('suppliers/create/', views.add_supplier.as_view(), name='create-supplier'),
    path('suppliers/<int:pk>/edit/', views.edit_supplier.as_view(), name='edit-supplier'),
    path('suppliers/<int:id>/', views.supplier_details, name='supplier-details'),

    # Other URLs
    path('add-returns/', views.add_returns_view.as_view(), name='add-returns'),
    path('invoice-payments/', views.InvoicePayment_view, name='invoice-payments'),
    path('add-payment/', views.add_payment_view.as_view(), name='add-payment'),
    path('edit-payment/<int:pk>/', views.edit_payment_view.as_view(), name='edit-payment'),
    path('add-purchase-payments/', views.add_purchase_payment_view.as_view(), name='add-purchase-payments'),
    path('edit-purchase-payment/<int:pk>/', views.edit_purchase_payment_view.as_view(), name='edit-purchase-payment'),
    path('get_product_price/', views.get_product_price, name='get_product_price'),
    path('get_customer_name/', views.get_customer_name, name='get_customer_name'),
    path('add_more_row/', views.add_more_row, name='add_more_row'),
    path('add_more_row_purchase/', views.add_more_row_purchase, name='add_more_row_purchase'),
]