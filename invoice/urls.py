from django.urls import path
from . import views
from user.utils import login_required_patterns


app_name = 'invoice'

urlpatterns = [
    path('', views.invoice_view, name='invoice'),
    #path('view_invoice/', views.view_invoice, name='view_invoice'),
    path('create-invoice/', views.create_invoice, name='create-invoice'),
    path('create-purchase/', views.create_purchase, name='create-purchase'),
    #path('delete_invoice/<int:pk>/', views.delete_invoice, name='delete_invoice'),
    path('view_invoice_detail/<int:pk>/', views.invoice_detail, name='view_invoice_detail'),

    path('add-returns/', views.add_returns_view.as_view(), name='add-returns'),

    path('invoice-payments/', views.InvoicePayment_view, name='invoice-payments'),
    path('edit-payment/<int:pk>/', views.edit_payment_view.as_view(), name='edit-payment'),
    path('add-payment/', views.add_payment_view.as_view(), name='add-payment'),
    #for ajax
    path('get_product_price/', views.get_product_price, name='get_product_price'),
    path('customer/search/', views.search_customers, name='search_customers'), 
    path('add_more_row/', views.add_more_row, name='add_more_row'),
    path('get_customer_name/', views.get_customer_name, name='get_customer_name'),


]
urlpatterns = login_required_patterns(urlpatterns)