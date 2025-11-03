from django.urls import path
from .views import BoulangerieCustomerListView, BoulangerieCustomerDetailView, BoulangerieCustomerCreateView, BoulangerieCustomerEditView
from .views import (
    BoulangerieProductCategoryListView,
    BoulangerieProductCategoryDetailView,
    BoulangerieProductCategoryCreateView,
    BoulangerieProductCategoryEditView,
    
    # BoulangerieProductionListView,
    BoulangerieInventoryDetailView,
    #create_production,
)
from .views import (
    BoulangerieCustomerOpeningBalanceListView,
    BoulangerieCustomerOpeningBalanceCreateView,
    BoulangerieCustomerOpeningBalanceUpdateView,
    # BoulangerieReturnsItemsListView,
    # BarInventoryDetailView,

    # BoulangerieReturnsItemsCreateView,
    # BoulangerieReturnsItemsUpdateView,
)

from . import views
from .views import BoulangerieProductListView, BoulangerieProductCreateView, BoulangerieProductUpdateView
# from .views import ProductRecipeListView, ProductRecipeCreateView, ProductRecipeUpdateView
# from .views import RecipeRawMaterialListView, RecipeRawMaterialCreateView, RecipeRawMaterialUpdateView
# from .views import RawMaterialsListView, RawMaterialsCreateView, RawMaterialsUpdateView




app_name = 'boulangerie'

urlpatterns = [
     path('', views.boulangerie_view, name='boulangerie'),

##Customers
    path('customers/', BoulangerieCustomerListView.as_view(), name='customer'),
    path('customers/add/', BoulangerieCustomerCreateView.as_view(), name='customer-add'),  # New URL for adding customers
    path('customers/<slug:slug>/', BoulangerieCustomerDetailView.as_view(), name='customer-detail'),  # Detail view URL
    path('edit/<slug:slug>/', BoulangerieCustomerEditView.as_view(), name='customer-edit'),  # Edit customer URL
    
 ##Categories
    path('categories', BoulangerieProductCategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', BoulangerieProductCategoryDetailView.as_view(), name='category-detail'),
    path('categories/add/', BoulangerieProductCategoryCreateView.as_view(), name='category-create'),
    path('categories/edit/<int:pk>/', BoulangerieProductCategoryEditView.as_view(), name='category-edit'),


    # Invoices
    path('invoices/', views.invoice_view, name='invoice'),
    path('invoices/create/', views.create_invoice, name='create-invoice'),
    path('invoices/<int:pk>/view/', views.invoice_detail, name='view_invoice_detail'),
    path('invoices/edit/<int:pk>/', views.edit_invoice, name='edit_invoice'),
    # ... other invoice-related URLs

    # Purchases
    path('purchases/', views.purchases_view, name='purchases'),
    path('purchases/create/', views.create_purchase, name='create-purchase'),
    path('purchases/<int:pk>/view/', views.purchase_detail, name='purchase_detail'),
    path('purchases/edit/<int:pk>/', views.edit_purchase, name='edit-purchase'),

    # ... other purchase-related URLs

    #Products
    path('products/', BoulangerieProductListView.as_view(), name='product-list'),
    path('products/add/', BoulangerieProductCreateView.as_view(), name='product-add'),
    path('products/edit/<int:pk>/', BoulangerieProductUpdateView.as_view(), name='product-edit'),

    # Suppliers
    path('suppliers/', views.suppliers_view, name='supplier'),
    path('suppliers/create/', views.add_supplier.as_view(), name='create-supplier'),
    path('suppliers/<int:pk>/edit/', views.edit_supplier.as_view(), name='edit-supplier'),
    path('suppliers/<int:id>/', views.supplier_details, name='supplier-details'),

    # Inventories
    path('inventories/', views.inventory_view, name='Inventories'),
    path('inventories/create/', views.create_inventory, name='create_Inventory'),
    path('inventories/<int:pk>/', BoulangerieInventoryDetailView.as_view(), name='inventory-detail'),
    path('inventories/edit/<int:pk>/', views.edit_inventory, name='edit-inventory'),

    # ... other invoice-related URLs
 
    # Production
#     path('production/', BoulangerieProductionListView.as_view(), name='production'),
#     path('production/create/', views.create_production, name='create-production'),
#     path('production/create_out/', views.create_production_out, name='create-out'),
#     path('add_more_row_production/', views.add_more_row_production, name='add_more_row_production'),
#     path('add_more_row_output/', views.add_more_row_output, name='add_more_row_output'),
# #Recipes
#     path('product-recipes/', ProductRecipeListView.as_view(), name='productrecipe-list'),
#     path('product-recipe/add/', ProductRecipeCreateView.as_view(), name='productrecipe-add'),
#     path('product-recipe/edit/<int:pk>/', ProductRecipeUpdateView.as_view(), name='productrecipe-edit'),
# #raw materials
#     path('raw-materials-list/', RawMaterialsListView.as_view(), name='raw-materials-list'),
#     path('raw-materials-add/', RawMaterialsCreateView.as_view(), name='raw-materials-add'),
#     path('raw-materials-edit/<int:pk>/edit/', RawMaterialsUpdateView.as_view(), name='raw-materials-edit'),
 
# #Recipe Raw materials
#     path('recipe-raw-materials/', RecipeRawMaterialListView.as_view(), name='reciperawmaterial-list'),
#     path('recipe-raw-material/add/', RecipeRawMaterialCreateView.as_view(), name='reciperawmaterial-add'),
#     path('recipe-raw-material/edit/<int:pk>/', RecipeRawMaterialUpdateView.as_view(), name='reciperawmaterial-edit'),
    # Customer Opening Balance
    path('customer-opening-balance/', BoulangerieCustomerOpeningBalanceListView.as_view(), name='customer-opening-balance-list'),
    path('customer-opening-balance/add/', BoulangerieCustomerOpeningBalanceCreateView.as_view(), name='customer-opening-balance-add'),
    path('customer-opening-balance/edit/<int:pk>/', BoulangerieCustomerOpeningBalanceUpdateView.as_view(), name='customer-opening-balance-edit'),

    # Customer Return Items
    # path('return-items/', BoulangerieReturnsItemsListView.as_view(), name='customer-return-items-list'),
    # path('add-returns/', views.add_returns_view.as_view(), name='customer-return-items-add'),
    # path('customer-return-items/edit/<int:pk>/', BoulangerieReturnsItemsUpdateView.as_view(), name='customer-return-items-edit'),

   
    path('invoice-payments/', views.InvoicePayment_view, name='invoice-payments'),
    path('add-payment/', views.add_payment_view.as_view(), name='add-payment'),
    path('edit-payment/<int:pk>/', views.edit_payment_view.as_view(), name='edit-payment'),

    # Other URLs
    path('add-purchase-payments/', views.add_purchase_payment_view.as_view(), name='add-purchase-payments'),
    path('edit-purchase-payment/<int:pk>/', views.edit_purchase_payment_view.as_view(), name='edit-purchase-payment'),
    path('get_product_price/', views.get_product_price, name='get_product_price'),
    path('get_raw_price/', views.get_raw_price, name='get_raw_price'),
    path('get_customer_name/', views.get_customer_name, name='get_customer_name'),
    path('add_more_row/', views.add_more_row, name='add_more_row'),
    path('add_more_row_purchase/', views.add_more_row_purchase, name='add_more_row_purchase'),
    # path('add_more_row_inventory/', views.add_more_row_inventory, name='add_more_row_inventory'),
    
]