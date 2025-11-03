from django.urls import path
from . import views

app_name = 'customer'


urlpatterns = [
    path('', views.customer, name='customer'),
    path('create-customer/', views.add_customer.as_view(), name='create-customer'),
    path('edit-customer/<int:pk>/', views.edit_customer.as_view(), name='edit-customer'),
    path('customer-details/<slug:slug>/', views.customer_details, name='customer-details'),

]
