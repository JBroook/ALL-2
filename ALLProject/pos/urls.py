from django.urls import path
from . import views


appname = 'pos'
urlpatterns = [
    path('sales/', views.cashierPOSView, name="sales"),
    path('history/',views.cashierHistoryView, name="history")
]