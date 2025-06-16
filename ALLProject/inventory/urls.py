from django.urls import path
from . import views


appname = 'inventory'
urlpatterns = [
    path('product_list/', views.product_list_view, name="product_list"),
    path('product_list_partial/', views.product_list_partial_view, name="product_list_partial"),
    path('product_create/', views.product_create_view, name="product_create"),
    path('product_info/<int:product_id>/', views.product_info_view, name="product_info"),
    path('product_update/<int:product_id>/',views.product_update_view, name="product_update"),
    path('product_delete/<int:product_id>/', views.product_delete_view, name="product_delete"),
    path('product_restock/<int:product_id>/', views.product_restock_view, name="product_restock"),
    path('product_print/<int:product_id>/', views.product_print_view, name="product_print"),
    path('restock_order/', views.restock_order_view, name="restock_order"),
    path('category/', views.category_view, name="category"),
    path('category_partial/', views.category_partial_view, name="category_partial"),
    path('category_form/', views.category_form_view, name="category_form"),
    path('category_create/', views.category_create_view, name="category_create"),
    path('category_specific/<int:category_id>/', views.category_specific_view, name="category_specific"),
    path('category_delete/<int:category_id>/', views.category_delete_view, name="category_delete"),
    path('category_edit/<int:category_id>/', views.category_edit_view, name="category_edit"),
]
