from django.urls import path
# from .views import BarCustomerListView, BarCustomerDetailView, BarCustomerCreateView, BarCustomerEditView
from .views import (
    BarProductCategoryListView,
    BarProductCategoryDetailView,
    BarProductCategoryCreateView,
    BarProductCategoryEditView,
    
    # BarProductionListView,
    BarInventoryDetailView,
    #create_production,
)
from . import views
from .views import BarProductListView, BarProductCreateView, BarProductUpdateView




app_name = 'bar'

urlpatterns = [
     path('', views.bar_view, name='bar'),

##Customers
    # path('customers/', BarCustomerListView.as_view(), name='customer'),
    # path('customers/add/', BarCustomerCreateView.as_view(), name='customer-add'),  # New URL for adding customers
    # path('customers/<slug:slug>/', BarCustomerDetailView.as_view(), name='customer-detail'),  # Detail view URL
    # path('edit/<slug:slug>/', BarCustomerEditView.as_view(), name='customer-edit'),  # Edit customer URL
    
 ##Categories
    path('categories', BarProductCategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', BarProductCategoryDetailView.as_view(), name='category-detail'),
    path('categories/add/', BarProductCategoryCreateView.as_view(), name='category-create'),
    path('categories/edit/<int:pk>/', BarProductCategoryEditView.as_view(), name='category-edit'),
#Products
    path('products/', BarProductListView.as_view(), name='product-list'),
    path('products/add/', BarProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/edit/', BarProductUpdateView.as_view(), name='product-edit'),  # Use ID (pk) for editing


    # # Invoices
    # path('invoices/', views.invoice_view, name='invoice'),
    # path('invoices/create/', views.create_invoice, name='create-invoice'),
    # path('invoices/<int:pk>/view/', views.invoice_detail, name='view_invoice_detail'),
    # # ... other invoice-related URLs

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

    # Inventories
    path('inventories/', views.inventory_view, name='Inventories'),
    path('inventories/create/', views.create_inventory, name='create_Inventory'),
    path('inventories/<int:pk>/', BarInventoryDetailView.as_view(), name='inventory-detail'),
    path('inventories/edit/<int:pk>/', views.edit_inventory, name='edit-inventory'),
    # ... other invoice-related URLs
 
    # # Production
    # path('production/', BarProductionListView.as_view(), name='production'),
    # path('production/create/', views.create_production, name='create-production'),
    # path('production/create_out/', views.create_production_out, name='create-out'),
    # path('add_more_row_production/', views.add_more_row_production, name='add_more_row_production'),
    # path('add_more_row_output/', views.add_more_row_output, name='add_more_row_output'),

    # Other URLs
    # path('add-returns/', views.add_returns_view.as_view(), name='add-returns'),
    # path('invoice-payments/', views.InvoicePayment_view, name='invoice-payments'),
    # path('add-payment/', views.add_payment_view.as_view(), name='add-payment'),
    # path('edit-payment/<int:pk>/', views.edit_payment_view.as_view(), name='edit-payment'),
    # path('add-purchase-payments/', views.add_purchase_payment_view.as_view(), name='add-purchase-payments'),
    # path('edit-purchase-payment/<int:pk>/', views.edit_purchase_payment_view.as_view(), name='edit-purchase-payment'),
    path('get_product_price/', views.get_product_price, name='get_product_price'),
    # path('get_raw_price/', views.get_raw_price, name='get_raw_price'),
    # path('get_customer_name/', views.get_customer_name, name='get_customer_name'),
    # path('add_more_row/', views.add_more_row, name='add_more_row'),
    path('add_more_row_purchase/', views.add_more_row_purchase, name='add_more_row_purchase'),
    path('add_more_row_inventory/', views.add_more_row_inventory, name='add_more_row_inventory'),
    
]