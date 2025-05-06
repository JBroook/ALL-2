from django.urls import path
from . import views


appname = 'inventory'
urlpatterns = [
    path('product_list/', views.product_list_view, name="product_list"),
    path('product_list2/', views.product_list_view2, name="product_list2"),
]