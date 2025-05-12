from django.urls import path
from . import views


appname = 'inventory'
urlpatterns = [
    path('product_list/', views.product_list_view, name="product_list"),
    path('product_create/', views.product_create_view, name="product_create"),
    path('product_update/<int:product_id>/',views.product_update_view, name="product_update"),
    path('product_delete/<int:product_id>/', views.product_delete_view, name="product_delete"),
]