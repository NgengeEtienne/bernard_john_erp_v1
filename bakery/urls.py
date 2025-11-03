from django.urls import path
from .views import BakeryCustomerListView, BakeryCustomerDetailView, BakeryCustomerCreateView, BakeryCustomerEditView
from .views import (
    BakeryProductCategoryListView,
    BakeryProductCategoryDetailView,
    BakeryProductCategoryCreateView,
    BakeryProductCategoryEditView,
    
    BakeryProductionListView,
    BakeryInventoryDetailView,
    #create_production,
)
from .views import (
    BakeryCustomerOpeningBalanceListView,
    BakeryCustomerOpeningBalanceCreateView,
    BakeryCustomerOpeningBalanceUpdateView,
    BakeryReturnsItemsListView,
    # BakeryReturnsItemsCreateView,
    BakeryReturnsItemsUpdateView,
    payment_details_view,
)

from . import views
from .views import BakeryProductListView, BakeryProductCreateView, BakeryProductUpdateView
from .views import ProductRecipeListView, ProductRecipeCreateView, ProductRecipeUpdateView
from .views import RawMaterialsListView, RawMaterialsCreateView, RawMaterialsUpdateView
from .views import RecipeListView, RecipeCreateView, RecipeUpdateView




app_name = 'bakery'

urlpatterns = [
     path('', views.bakery_view, name='bakery'),

##Customers
    path('customers/', BakeryCustomerListView.as_view(), name='customer'),
    path('customers/add/', BakeryCustomerCreateView.as_view(), name='customer-add'),  # New URL for adding customers
    path('customers/<slug:slug>/', BakeryCustomerDetailView.as_view(), name='customer-detail'),  # Detail view URL
    path('edit/<slug:slug>/', BakeryCustomerEditView.as_view(), name='customer-edit'),  # Edit customer URL
    
 ##Categories
    path('categories', BakeryProductCategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', BakeryProductCategoryDetailView.as_view(), name='category-detail'),
    path('categories/add/', BakeryProductCategoryCreateView.as_view(), name='category-create'),
    path('categories/edit/<int:pk>/', BakeryProductCategoryEditView.as_view(), name='category-edit'),


    # Invoices
    path('invoices/', views.invoice_view, name='invoice'),
    path('invoices/returns/', views.returns_view, name='returns'),
    path('invoices/create/', views.create_invoice, name='create-invoice'),
    path('invoices/<int:pk>/view/', views.invoice_detail, name='view_invoice_detail'),
    path('invoices/edit/<int:pk>/', views.edit_invoice, name='edit_invoice'),
    # ... other invoice-related URLs


    # Damages
    path('damages/', views.damages_view, name='damages'),
    path('damages/create/', views.create_damages, name='create-damages'),
    path('damages/<int:pk>/view/', views.damages_detail, name='view_damages_detail'),
    path('damages/edit/<int:pk>/', views.edit_damage, name='edit_damages'),

    # Purchases
    path('purchases/', views.purchases_view, name='purchases'),
    path('purchases/create/', views.create_purchase, name='create-purchase'),
    path('purchases/<int:pk>/view/', views.purchase_detail, name='purchase_detail'),
    path('purchases/edit/<int:pk>/', views.edit_purchase, name='edit-purchase'),
    # ... other purchase-related URLs

    #Products
    path('products/', BakeryProductListView.as_view(), name='product-list'),
    path('products/add/', BakeryProductCreateView.as_view(), name='product-add'),
    path('products/edit/<int:pk>/', BakeryProductUpdateView.as_view(), name='product-edit'),

    # Suppliers
    path('suppliers/', views.suppliers_view, name='supplier'),
    path('suppliers/create/', views.add_supplier.as_view(), name='create-supplier'),
    path('suppliers/<int:pk>/edit/', views.edit_supplier.as_view(), name='edit-supplier'),
    path('suppliers/<int:id>/', views.supplier_details, name='supplier-details'),

    # Inventories
    path('inventories/', views.inventory_view, name='Inventories'),
    path('inventories/create/', views.create_inventory, name='create_Inventory'),
    path('inventories/<int:pk>/', BakeryInventoryDetailView.as_view(), name='inventory-detail'),
    path('inventories/edit/<int:pk>/', views.edit_inventory, name='edit-inventory'),

    # ... other invoice-related URLs
  
    # Production
    path('production/', BakeryProductionListView.as_view(), name='production'),
    path('production/create/', views.create_production, name='create-production'),
    path('production/edit_out/<int:pk>/', views.edit_production_out, name='edit-out'),
    path('production/create_out/', views.create_production_out, name='create-out'),
    path('production/<int:pk>/view/', views.production_detail, name='view_production_detail'),
    path('production/edit/<int:pk>/', views.edit_production, name='edit_production'),
    path('add_more_row_production/', views.add_more_row_production, name='add_more_row_production'),
    path('add_more_row_output/', views.add_more_row_output, name='add_more_row_output'),

    #ajax
    path('bakery_production_list/', views.bakery_production_list, name='bakery_production_list'),
#Recipes
    path('product-recipes/', ProductRecipeListView.as_view(), name='productrecipe-list'),
    path('product-recipe/add/', ProductRecipeCreateView.as_view(), name='productrecipe-add'),
    path('product-recipe/edit/<int:pk>/', ProductRecipeUpdateView.as_view(), name='productrecipe-edit'),
#raw materials
    path('raw-materials-list/', RawMaterialsListView.as_view(), name='raw-materials-list'),
    path('raw-materials-add/', RawMaterialsCreateView.as_view(), name='raw-materials-add'),
    path('raw-materials-edit/<int:pk>/edit/', RawMaterialsUpdateView.as_view(), name='raw-materials-edit'),

#Recipe Raw materials
    path('recipe-raw-materials/', views.recipe_raw_material_list_view, name='reciperawmaterial-list'),
    path('recipe-raw-material/add/', views.create_recipe_raw_material, name='reciperawmaterial-add'),
    path('recipe-raw-material/edit/<int:pk>/', views.edit_recipe_raw_material, name='reciperawmaterial-edit'),
    # Customer Opening Balance
    path('customer-opening-balance/', BakeryCustomerOpeningBalanceListView.as_view(), name='customer-opening-balance-list'),
    path('customer-opening-balance/add/', BakeryCustomerOpeningBalanceCreateView.as_view(), name='customer-opening-balance-add'),
    path('customer-opening-balance/edit/<int:pk>/', BakeryCustomerOpeningBalanceUpdateView.as_view(), name='customer-opening-balance-edit'),

    path('recipes/', RecipeListView.as_view(), name='recipes'),
    path('recipes/add/', RecipeCreateView.as_view(), name='recipes_add'),
    path('recipes/edit/<int:pk>/', RecipeUpdateView.as_view(), name='recipes_edit'),
    # Production output
    path('production/recipe/',views.production_output, name='productioin_output'),
    path('get_production_recipe/', views.get_production_recipe, name='get_production_recipe'),
    # path('add-returns/', views.add_returns_view.as_view(), name='customer-return-items-add'),
    # path('customer-return-items/edit/<int:pk>/', BakeryReturnsItemsUpdateView.as_view(), name='customer-return-items-edit'),
    path('recipe/', views.recipe, name='recipe'),
    path('get_recipe/', views.get_recipe, name='get_recipe'),
    path('invoice-payments/', views.InvoicePayment_view, name='invoice-payments'),
    path('add-payment/', views.add_payment_view.as_view(), name='add-payment'),
    path('edit-payment/<int:pk>/', views.edit_payment_view.as_view(), name='edit-payment'),
    path('payment-details/<int:pk>/', views.payment_details_view, name='payment-details'),
    # Other URLs
    path('add-purchase-payments/', views.add_purchase_payment_view.as_view(), name='add-purchase-payments'),
    path('edit-purchase-payment/<int:pk>/', views.edit_purchase_payment_view.as_view(), name='edit-purchase-payment'),
    path('get_product_price/', views.get_product_price, name='get_product_price'),
    path('get_raw_price/', views.get_raw_price, name='get_raw_price'),
    path('get_customer_name/', views.get_customer_name, name='get_customer_name'),
    path('add_more_row/', views.add_more_row, name='add_more_row'),
    path('add_more_row_purchase/', views.add_more_row_purchase, name='add_more_row_purchase'),
    path('add_more_row_inventory/', views.add_more_row_inventory, name='add_more_row_inventory'),
    path('add_more_row_recipe/', views.add_more_row_Recipe_rawmaterial, name='add_more_row_recipe'),
    path('add_more_row_damage/', views.add_more_row_damage, name='add_more_row_damage'),
    #REPORTS
    path('inventory-report/', views.inventory_report, name='inventory_report'),
    path('get-inventory-report/', views.get_inventory_report, name='get_inventory_report'),

    path('production-report/', views.production_report, name='production_report'),
    path('get-production-report/', views.get_production_report, name='get_production_report'),

]