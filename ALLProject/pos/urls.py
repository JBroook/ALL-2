from django.urls import path
from . import views


appname = 'pos'
urlpatterns = [
    path('sales/', views.cashierPOSView, name="sales"),
    path('history/',views.cashierHistoryView, name="history"),
    path('history_partial/<str:type>/',views.cashierHistoryPartialView, name="history_partial"),
    path('date_filter/',views.date_filter_view, name="date_filter"),
    path('details/<int:payment_id>/',views.payment_detail_view, name="payment_details"),
    path('call_manager/', views.call_manager_view, name='call_manager'),
    path('print_payment/<int:payment_id>/', views.print_payment_view, name='print_payment'),
]