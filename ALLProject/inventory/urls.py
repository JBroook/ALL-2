from django.urls import path
from . import views


appname = 'inventory'
urlpatterns = [
    path('product_list/', views.product_list_view, name="product_list"),
    path('product_table/', views.product_table_view, name="product_table"),
    path('product_create/', views.product_create_view, name="product_create"),
    path('product_update/<int:product_id>/',views.product_update_view, name="product_update"),
    path('product_delete/<int:product_id>/', views.product_delete_view, name="product_delete"),
    path('product_restock/<int:product_id>/', views.product_restock_view, name="product_restock"),
    path('restock_order/', views.restock_order_view, name="restock_order"),
    path('product_table_partial/', views.product_table_partial_view, name="product_table_partial"),
]