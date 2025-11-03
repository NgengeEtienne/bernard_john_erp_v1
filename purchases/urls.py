from django.urls import path
from . import views


app_name = 'purchases'

urlpatterns = [
    path('', views.purchases_view, name='purchases'),
    path('view_purchase_detail/<int:pk>/', views.purchase_detail, name='view_purchase_detail'),
    path('create-purchase/', views.create_purchase, name='create-purchase'),

    path('purchase-invoice-payments/', views.purchase_invoice_payments_view, name='purchase-invoice-payments'),
    path('add-purchase-payments/', views.add_purchase_payment_view.as_view(), name='add-purchase-payments'),
    path('edit-purchase-payment/<int:pk>/', views.edit_purchase_payment_view.as_view(), name='edit-purchase-payment'),
    #ajax
    path('get_product_price/', views.get_product_price, name='get_product_price'),
    #path('customer/search/', views.search_customers, name='search_customers'), 
    path('add_more_row/', views.add_more_row, name='add_more_row'),
    #path('get_customer_name/', views.get_customer_name, name='get_customer_name'),


]
