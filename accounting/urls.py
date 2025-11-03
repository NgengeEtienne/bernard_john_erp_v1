from django.urls import path
from . import views

app_name = 'accounting'
urlpatterns = [
    path('', views.accounting_view, name='accounting'),
    path('accounts_category/', views.accounts_category, name='accounts_category'),
    path('accounts_category_edit/<pk>/', views.accounts_category_edit, name='accounts_category_edit'),
    path('accounts_category/add/', views.accounts_category_add, name='accounts_category_add'),
    path('accounts_sub_category/', views.accounts_sub_category, name='accounts_sub_category'),
    path('accounts_sub_category_edit/<pk>/', views.accounts_sub_category_edit, name='accounts_sub_category_edit'),
    path('accounts_sub_category/add/', views.accounts_sub_category_add, name='accounts_sub_category_add'),
    path('accounts_debit/', views.accounts_debit, name='accounts_debit'),
    path('accounts_debit_edit/<pk>/', views.accounts_debit_edit, name='accounts_debit_edit'),
    path('accounts_debit/add/', views.accounts_debit_add, name='accounts_debit_add'),
    path('accounts_credit/', views.accounts_credit, name='accounts_credit'),
    path('accounts_credit_edit/<pk>/', views.accounts_credit_edit, name='accounts_credit_edit'),
    path('accounts_credit/add/', views.accounts_credit_add, name='accounts_credit_add'),
    path('<str:department>/general-ledger/', views.general_ledger_view, name='department_general_ledger'),
    path('<str:department>/general-ledger/edit/<pk>/', views.general_ledger_edit, name='department_general_ledger_edit'),
    path('<str:department>/general-ledger/add/', views.general_ledger_add, name='department_general_ledger_add'),

    path('<str:department>/add_more_row_general_ledger/', views.add_more_row, name='add_more_row_general_ledger'),

]
